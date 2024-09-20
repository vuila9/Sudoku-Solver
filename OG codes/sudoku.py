import math
import os
import random

'''
RULES
Rule 1: Each row must contain the numbers from 1 to 9, without repetitions
Rule 2: Each column must contain the numbers from 1 to 9, without repetitions
Rule 3: The digits can only occur once per block (nonet)
'''

def printSudoku(sud) -> None: #print any 9x9 sudoku board in a nicely format
    for row in range(len(sud)):
        if row != 0 and row %3 == 0:
            print("------+-------+------")
        for col in range(len(sud[row])):
            if col != 0 and col %3 == 0:
                print("|", end=" ")
            print(sud[row][col], end=" ")
        print()

def verifySudoku(sud) -> bool: #verify if sudoku starting state is valid as well as solution, does not detect unsolvable sudoku board
    def verifySet(arr) -> bool:
        st = set(arr)
        st.discard(0)
        arr = [x for x in arr if x != 0]
        for numb in arr:
            if 1 > numb or numb > 9:
                print("Input number out of range 1-9")
                return False
        return len(arr) == len(st)
    
    # Verifying rule 1:
    for row in range(len(sud)):
        
        if not verifySet(sud[row]):
            print("Rule 1 not satisfied")
            return False

    # Verifying rule 2:
    for row in range(len(sud)):
        coln = []
        for col in range(len(sud[row])):
            coln.append(sud[col][row])
        if not verifySet(coln):
            print("Rule 2 not satisfied")
            return False

    # Verifying Rule 3:
    for row in range(len(sud)):
        block = []
        for col in range(len(sud[row])):
            block.append(sud[(row // 3)*3 + col // 3][col % 3 + (row % 3) * 3])
        if not verifySet(block):
            print("Rule 3 not satisfied")
            return False
              
    return True

def transpose(sud) -> list: #return matrix of sudoku board but column wise
    transpose_sud = []
    for row in range(len(sud)):
        coln = []
        for col in range(len(sud[row])):
            coln.append(sud[col][row])    
        transpose_sud.append(coln)
    return transpose_sud

def blockerize(sud) -> list: #return matrix of sudoku board but block wise
    blockerize_sud = []
    for row in range(len(sud)):
        block = []
        for col in range(len(sud[row])):
            block.append(sud[(row // 3)*3 + col // 3][col % 3 + (row % 3) * 3])   
        blockerize_sud.append(block)
    return blockerize_sud

def fixedlocation(sud) -> list: #return a set of fixed location of tiles from starting sudoku board
    fixed = []
    for row in range(len(sud)):
        for col in range(len(sud[row])):
            if sud[row][col] != 0:
                fixed.append(str(row) + str(col))
    return fixed

def write_record(log, mode) -> None: #transfer console log to a text file, use 'a' to not erase when rewrite
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, 'output.txt')
    with open(file_path, mode) as file: # open in "w" (write mode) will automatically erase the content when first open
        file.write("{}\n".format(log))

def wrap_number(num) -> int: #will add 1 to input number and return number from 1-9
    return (num % 9) or 9

def isValid(sud, row, col, value) -> bool: #check if for current row, column, the input value is acceptable according to the rules
    for i in range(9):
        if sud[i][col] == value or sud[row][i] == value:
            return False

        block_row = 3 * (row // 3) + i//3
        block_col = 3 * (col // 3) + i%3
        if sud[block_row][block_col] == value:
            return False
    
    return True

def spawn(difficulty) -> list: #spawn any 9x9 sudoku board with empty tiles to solve, will pass verifySudoku but could also end up unsolvable
    sud = [[0 for _ in range(9)] for _ in range(9)]
    numb = [1,2,3,4,5,6,7,8,9]
    rate = 0
    if difficulty == "EXPERT":
        rate = 9
    elif difficulty == "HARD":
        rate = 15
    elif difficulty == "MEDIUM":
        rate = 21
    elif difficulty == "EASY":
        rate = 30
    for row in range(9):
        for col in range(9):
            if random.uniform(0,100) < rate:              
                val = random.choice(numb)
                counter = 0
                while counter < 9:
                    if isValid(sud, row, col, val):
                        sud[row][col] = val
                        break
                    val = ((val + 1) %9) or 9
                    counter +=1  
                continue                  
            
    return sud

def howIwouldsolve(sud) -> list: #noobie strat cannot solve any sudoku, maybe 1 idk
    counter = 0
    fixed = []
    blockerize_sud = transpose_sud = []
    for row in range(len(sud)):
        blockerize_sud = blockerize(sud)
        transpose_sud = transpose(sud)
        for col in range(len(sud[row])):
            sud_row = set(sud[row])
            if sud[row][col] != 0:
                fixed.append(str(row) + str(col))
                continue
            sud_col = set(transpose_sud[col])
            sud_block = set(blockerize_sud[(row // 3)*3 + col // 3])
            union = sud_row | sud_col | sud_block
            for i in range(1,10):
                if i not in union:
                    sud[row][col] = i
                    break  
    return sud

def backtracking(sud): #can detect unsolvable sudoku (?), but takes really long time to solve any sudoku
    row, col = 0, 0
    beginning_coor = "99"
    fixed_sud = set(fixedlocation(sud))
    row_backtrack, col_backtrack = False, False
    while -1 < row and row < 9:
        col = 8 if row_backtrack else 0

        while -1 < col and col < 9:
            if (str(row) + str(col)) in fixed_sud:
                if col_backtrack:
                    col -=1
                    if col < 0:
                        row_backtrack = True
                else:
                    col +=1
                continue

            temp = sud[row][col]
            start = sud[row][col] + 1
            for i in range(start, 10):
                if isValid(sud, row, col, i):
                    if beginning_coor == "99":
                        beginning_coor = str(col) + str(row)
                    sud[row][col] = i
                    col_backtrack = False
                    row_backtrack = False
                    break

            if sud[row][col] == temp: #fail to find any number, start backtracking
                sud[row][col] = 0
                col_backtrack = True

                if row == int(beginning_coor[0]) and col == int(beginning_coor[1]): # at beginning slot but still no valid solution --> maybe no solution
                    print("No possible solution") # sometimes the detection is incorrect
                    return sud

            if col_backtrack:
                col -=1
                if col < 0:
                    row_backtrack = True
            else:
                col +=1
        
        if row_backtrack:
            row -=1
        else:
            row +=1
    
    return sud

def recursive_backtracking(sud, row, col):  #cannot detect unsolvable sudoku, can solve any sudoku in relatively fast runtime
    if row == 9:
        return True
    else:
        if col == 9:
            return recursive_backtracking(sud, row+1, 0)
        
        if sud[row][col] == 0:
            for i in range(1,10):
                if isValid(sud, row, col, i):
                    sud[row][col] = i
                    if recursive_backtracking(sud, row, col+1):
                        return True
                    sud[row][col] = 0
            return False
        
        return recursive_backtracking(sud, row, col+1)

def advanced_recursive_backtracking(sud): #WIP: the name says it, this is a recursive backtracking but with various of IRL advanced techniques for solving sudoku
    def findAllCandidate(sud) -> list:
        all_candidates = []
        for row in range(9):
            line = []
            for col in range(9):
                candidate = []
                if sud[row][col] == 0:
                    for i in range(1,10):
                        if isValid(sud, row, col, i):
                            candidate.append(i)
                    if len(candidate) == 0:
                        print("unsolvable soduku")
                line.append(candidate)
            all_candidates.append(line)
        
        return all_candidates

    def findNakedSingles(sud, all_candidates): #aka lone single
        for row in range(9):
            for col in range(9):
                if sud[row][col] == 0 and len(all_candidates[row][col]) == 1:
                    sud[row][col] = all_candidates[row][col][0]
                    all_candidates[row][col] = []

    def findHiddenSingles(sud, all_candidates):
        return 

    def findNakedPair(sud, all_candidates):
        return 

    def findNakedTriplet(sud, allcandidates):
        return 

    def omission(sud, allcandidates):
        return 

def dancing_links(sud): #WIP: can detect multiple solutions, the all-time fastest algorithm known to man for solving ANY 9x9 sudoku board with lightning fast runtime
    return 

def main() -> None:
    sudoku0 = [[0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0] 
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0]] #[0,0,0,0,0,0,0,0,0]

    sudoku1 = [[1,2,3,4,5,6,7,8,9], #[1,2,3,4,5,6,7,8,9]
               [7,8,9,1,2,3,4,5,6], #[7,8,9,1,2,3,4,5,6]
               [4,5,6,7,8,9,1,2,3], #[4,5,6,7,8,9,1,2,3]
               [3,1,2,8,4,5,9,6,7], #[3,1,2,8,4,5,9,6,7]
               [6,9,7,3,1,2,8,4,5], #[6,9,7,3,1,2,8,4,5]
               [8,4,5,6,9,7,3,1,2], #[8,4,5,6,9,7,3,1,2]
               [2,3,1,5,7,4,6,9,8], #[2,3,1,5,7,4,6,9,8]
               [9,6,8,2,3,1,5,7,4], #[9,6,8,2,3,1,5,7,4] 
               [5,7,4,9,6,8,2,3,1]] #[5,7,4,9,6,8,2,3,1]

    sudoku2 = [[0,0,0,0,0,0,0,0,4], #[0,0,0,0,0,0,0,0,4]
               [0,0,0,0,8,0,0,5,6], #[0,0,0,0,8,0,0,5,6]
               [2,0,0,0,0,0,0,0,0], #[2,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,7,0], #[0,0,0,0,0,0,0,7,0]
               [0,4,0,7,9,0,0,1,8], #[0,4,0,7,9,0,0,1,8]
               [6,0,0,0,2,3,0,0,9], #[6,0,0,0,2,3,0,0,9]
               [0,2,7,0,3,0,0,0,0], #[0,2,7,0,3,0,0,0,0]
               [0,0,4,0,0,0,0,0,0], #[0,0,4,0,0,0,0,0,0]
               [0,0,8,0,0,0,0,0,2]] #[0,0,8,0,0,0,0,0,2]
    
    sudoku3 = [[3,0,0,0,0,0,0,0,0], #[0,0,0,0,0,4,0,9,0]
               [0,7,0,0,0,0,0,0,0], #[8,0,2,9,7,0,0,0,0]
               [0,0,5,0,0,0,0,0,0], #[9,0,1,2,0,0,3,0,0]
               [0,0,0,3,0,0,0,0,0], #[0,0,0,0,4,9,1,5,7]
               [0,0,0,0,7,0,0,0,0], #[0,1,3,0,5,0,9,2,0]
               [0,0,0,0,0,5,0,0,0], #[5,7,9,1,2,0,0,0,0]
               [0,0,0,0,0,0,3,0,0], #[0,0,7,0,0,2,6,0,3]
               [0,0,0,0,0,0,0,7,0], #[0,0,0,0,3,8,2,0,5]
               [0,0,0,0,0,0,0,0,5]] #[0,2,0,5,0,0,0,0,0]
    
    sudoku5 = [[8,0,0,0,0,0,0,0,0], #[0,0,0,0,0,4,0,9,0]
               [0,0,3,6,0,0,0,0,0], #[8,0,2,9,7,0,0,0,0]
               [0,7,0,0,9,0,2,0,0], #[9,0,1,2,0,0,3,0,0]
               [0,5,0,0,0,7,0,0,0], #[0,0,0,0,4,9,1,5,7]
               [0,0,0,0,4,5,7,0,0], #[0,1,3,0,5,0,9,2,0]
               [0,0,0,1,0,0,0,3,0], #[5,7,9,1,2,0,0,0,0]
               [0,0,1,0,0,0,0,6,8], #[0,0,7,0,0,2,6,0,3]
               [0,0,8,5,0,0,0,1,0], #[0,0,0,0,3,8,2,0,5]
               [0,9,0,0,0,0,4,0,0]] #[0,2,0,5,0,0,0,0,0]
    
    sudoku6 = [[0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0] //unsolvable
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,1,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [5,0,2,6,0,0,4,0,7], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,4,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,9,8,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,3,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,0,0,0,0,0,0]] #[0,0,0,0,0,0,0,0,0]
    
    sudoku7 = [[0,0,3,0,1,0,0,0,0], #[0,0,0,0,0,0,0,0,0] 
               [4,1,5,0,0,0,0,9,0], #[0,0,0,0,0,0,0,0,0]
               [2,0,6,5,0,0,3,0,0], #[0,0,0,0,0,0,0,0,0]
               [5,0,0,0,8,0,0,0,9], #[0,0,0,0,0,0,0,0,0]
               [0,7,0,9,0,0,0,3,2], #[0,0,0,0,0,0,0,0,0]
               [0,3,8,0,0,4,0,6,0], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,2,6,0,4,0,3], #[0,0,0,0,0,0,0,0,0]
               [0,0,0,3,0,0,0,0,8], #[0,0,0,0,0,0,0,0,0]
               [3,2,0,0,0,7,9,5,0]] #[0,0,0,0,0,0,0,0,0]

    board = sudoku7
    print("\n=======ORIGINAL======")
    printSudoku(board)
    print("\n========SOLVE========")
    
    if verifySudoku(board):
        recursive_backtracking(board, 0, 0)
        printSudoku(board)

    '''board = spawn("EASY") # as mentioned before, spawn() can generate an unsolvable sudoku board even when it passes the initial check
    if verifySudoku(board):
        backtracking(board)
        printSudoku(board)'''

if __name__ == "__main__":
    main()
