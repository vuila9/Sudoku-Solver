from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
import random

@dataclass
class SolveState:
    board_candidates: List[List[Set[int]]]
    is_finalized: List[List[bool]]

    def clone(self):
        board_candidates = [ [ set(cand_set) for cand_set in row] for row in self.board_candidates ]
        is_finalized = [ [ fn for fn in row] for row in self.is_finalized ]
        return SolveState(board_candidates, is_finalized)

def get_box_idx(row: int, col: int) -> int:
    return 3 * (row // 3) + col // 3

def init_group_sets(board: List[List[int]]):
    row_sets = [set() for i in range(9)]
    col_sets = [set() for i in range(9)]
    box_sets = [set() for i in range(9)]
    for row in range(9):
        for col in range(9):
            cur_cell = board[row][col]
            if cur_cell == 0:
                continue
            for group_set in [ row_sets[row], col_sets[col], box_sets[get_box_idx(row, col)]]:
                if cur_cell in group_set:
                    raise Exception("Invalid initial board")
                group_set.add(cur_cell)

    return row_sets, col_sets, box_sets

def init_board_candidates(board, row_sets, col_sets, box_sets):
    board_candidates = [ [None for col in range(9)] for row in range(9)]
    is_finalized     = [ [False for col in range(9)] for row in range(9)]

    for row in range(9):
        for col in range(9):
            # Simple case: board has this already defined.
            cur_entry = board[row][col]
            if cur_entry != 0:
                board_candidates[row][col] = { cur_entry }
                is_finalized[row][col]     = True
            else:
                board_candidates[row][col] = get_candidates([
                    row_sets[row], col_sets[col], box_sets[get_box_idx(row, col)] ])
                is_finalized[row][col]     = False # Set to false even if there's only one candidate.
    
    return board_candidates, is_finalized

def get_candidates(cand_sets: List[Set[int]]):
    candidates = set(map(int, range(1, 10)))
    for cand_set in cand_sets:
        candidates = candidates - cand_set
    return candidates

def solve(state: SolveState) -> Optional[SolveState]:
    debug = False
    # Level 2 solve algorithm: 
    # apply the winnow algorithm to remove deterministic candidates. 
    # then, select the cell with the smallest number of remaining candidates.
    # Guess one of the candidates, then re-apply the solve algorithm. If the
    # guess is correct, the solve algorithm will find a correct solution and return it.
    # Return that solution up the chain.
    # If the guess is incorrect, change your guess and repeat until you find the correct
    # value.
    is_valid, return_code = winnow(state)
    if debug:
        print("winnow return: ", return_code)
        #print_board(state)
    if not is_valid:
        return None

    # Find the cell with the smallest number of candidates, unless this board is finalized.
    min_candidate_cell = None
    min_candidates     = float('inf')
    is_finalized       = True
    for row in range(9):
        for col in range(9):
            if state.is_finalized[row][col]:
                assert len(state.board_candidates[row][col]) == 1
            else:
                is_finalized = False
                if len(state.board_candidates[row][col]) < min_candidates:
                    min_candidates = len(state.board_candidates[row][col])
                    min_candidate_cell = (row, col)

    # If we've finalized this board, return immediately
    if is_finalized:
        return state
    
    # Else there must have been some min_candidate_cell.
    assert min_candidate_cell != None
    min_cand_row, min_cand_col = min_candidate_cell

    for candidate_val in state.board_candidates[min_cand_row][min_cand_col]:
        # Duplicate the solve state and re-apply the winnow algorithm.
        guess_state = state.clone()
        guess_state.board_candidates[min_cand_row][min_cand_col] = { candidate_val }
        maybe_solved_state = solve(guess_state)
        if maybe_solved_state:
            return maybe_solved_state

    # If we reach this state the board is invalid
    return None

def winnow(state: SolveState) -> Tuple[bool, int]:
    # Simple solve algorithm:
    # Loop over the board and collect all non-finalized cells that have only
    # one candidate. Store them in a queue. 
    # While the queue is not empty, pop an entry off, finalize it, and 
    # remove it as a candidate for all squares in the same row, column, and box.
    # When removing, if any corresponding non-finalized cell has only one remaining
    # entry, add it to the queue. 
    # Once the queue is empty, check if everything is finalized. If not we'll need
    # to make some guesses... just throw for now and we can revisit.
    # Return True if the board remains in a valid state after winnowing, otherwise
    # return False. If this returns False, the winnowing process ends and the board
    # will be in an inconsistent state.
    single_candidate_cells = []
    for r in range(9):
        for c in range(9):
            if not state.is_finalized[r][c] and len(state.board_candidates[r][c]) == 1:
               single_candidate_cells.append((r, c))

    while len(single_candidate_cells) > 0:
        cur_row, cur_col = single_candidate_cells.pop()
        assert len(state.board_candidates[cur_row][cur_col]) == 1
        cur_val = next(iter(state.board_candidates[cur_row][cur_col]))

        state.is_finalized[cur_row][cur_col] = True

        # Remove cur_val as a candidate everywhere.
        # Remove from everything in this row
        for col in range(9):
            if state.is_finalized[cur_row][col]:
                continue
            if not maybe_remove_candidate_and_enqueue(cur_val, cur_row, col, state, single_candidate_cells):
                return False, 1
        
        # Remove from everything in this col
        for row in range(9):
            if state.is_finalized[row][cur_col]:
                continue
            if not maybe_remove_candidate_and_enqueue(cur_val, row, cur_col, state, single_candidate_cells):
                return False, 2

        # Remove from everything in this box
        for row, col in get_box_coords(cur_row, cur_col):
            if state.is_finalized[row][col]:
                continue
            if not maybe_remove_candidate_and_enqueue(cur_val, row, col, state, single_candidate_cells):
                return False, 3

    return True, 4

def maybe_remove_candidate_and_enqueue(cur_val: int, row: int, col: int, 
                                       state: SolveState, single_candidate_cells: List[Tuple[int, int]]) -> bool:
    '''
    Remove the current value from the candidates for the given cell, and append this cell to the single_candidates
    list if removing this value reduces the number of candidates to one.
    If removing this value reduces the number of candidates to zero, return False, as this means we've entered
    an invalid board state. Otherwise return True
    '''
    cur_candidates = state.board_candidates[row][col]
    if cur_val in cur_candidates:
        cur_candidates.remove(cur_val)
        if len(cur_candidates) == 1:
            single_candidate_cells.append((row, col))
        elif len(cur_candidates) == 0:
            return False
    return True

def get_box_coords(row: int, col: int):
    base_row = 3 * (row // 3) # 0, 3, 6
    base_col = 3 * (col // 3) # 0, 3, 6
    for r in range(base_row, base_row+3):
        for c in range(base_col, base_col+3):
            yield r, c

def print_sudoku(sud) -> None: #print any 9x9 sudoku board in a nicely format
    for row in range(len(sud)):
        if row != 0 and row %3 == 0:
            print("------+-------+------")
        for col in range(len(sud[row])):
            if col != 0 and col %3 == 0:
                print("|", end=" ")
            print(sud[row][col], end=" ")
        print()

def verify_sudoku(sud) -> bool: 
    # Verify if complete state of the sudoku is valid
    def verifySet(arr) -> bool:
        st = set(arr)
        #st.discard(0)
        arr = [x for x in arr if x != 0]
        for numb in arr:
            if 1 > numb or numb > 9:
                print("Input number out of range 1-9")
                return False
        return len(arr) == len(st)
    
    # Verifying rule 1:
    for row in range(len(sud)):
        if 0 in sud[row]:
            print("Incomplete board")
            return False
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

def solve_sudoku(board: List[List[int]]) -> Tuple[bool, str]:
    # First initialize our solve state
    try:
        row_sets, col_sets, box_sets = init_group_sets(board)
        board_candidates, is_finalized = init_board_candidates(board, row_sets, col_sets, box_sets)
        state = SolveState(board_candidates, is_finalized)
        # Solve
        solved_state = solve(state)
    except Exception as e:
        print("Invalid board\n")
        return False, "invalid"
    
    # Finally copy everything over to the original board and return.
    for row in range(9):
        for col in range(9):
            try:
                assert solved_state.is_finalized[row][col]
                assert len(solved_state.board_candidates[row][col]) == 1
                if board[row][col] == 0:
                    entry = next(iter(solved_state.board_candidates[row][col]))
                    board[row][col] = entry
            except Exception as e:
                print("Unsolvable sudoku\n")
                return False, "unsolvable"
    return True, ""

def limit_to_one_digit(P):
    """Allow only one digit or empty string"""
    if len(P) == 0:
        # empty Entry is ok
        return True
    elif len(P) == 1 and P.isdigit():
        # Entry with 1 digit is ok
        return True
    else:
        # Anything else, reject it
        return False

def spawn(difficulty) -> list: #spawn any 9x9 sudoku board with empty tiles to solve, might spawn an unsolvable board
    def isValid(sud, row, col, value) -> bool: #check if for current row, column, the input value is acceptable according to the rules
        for i in range(9):
            if sud[i][col] == value or sud[row][i] == value:
                return False
            block_row = 3 * (row // 3) + i//3
            block_col = 3 * (col // 3) + i%3
            if sud[block_row][block_col] == value:
                return False
        return True   
    
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