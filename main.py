import tkinter as tk
from tkinter import messagebox
import sudoku_penciling as sud
from tkinter import Toplevel
import copy

class SudokuGUI:
    def __init__(self, root, width=500, height=500):
        self.root = root
        self.root.title("Sudoku Game")
        self.grid = []
        self.sudoku_board = []
        self.create_grid()
        self.fixed_cells = set()
        self.solvable = False
        self.difficulty = ""

        
        self.center_window(width, height)
        self.root.resizable(False, False)


        # Add a button to submit the Sudoku grid
        self.submit_button = tk.Button(self.root, text="Submit", width=10, height=2, command=self.submit)
        self.submit_button.grid(row=1, column=10, columnspan=2)

        self.check_button = tk.Button(self.root, text="Check", width=10, height=2, command=self.check_board)
        self.check_button.grid(row=2, column=10, columnspan=2)
        self.check_button['state'] = "disable"

        self.solve_button = tk.Button(self.root, text="Solve", width=10, height=2, command=self.solve)
        self.solve_button.grid(row=3, column=10, columnspan=2)
        self.solve_button['state'] = "disable"

        self.reset_button = tk.Button(self.root, text="Reset", width=10, height=2, command=self.reset)
        self.reset_button.grid(row=4, column=10, columnspan=2)

        self.generate_button = tk.Button(self.root, text="Generate", width=10, height=2, command=self.generate)
        self.generate_button.grid(row=5, column=10, columnspan=2)
        #self.generate_button['state'] = "active"

        self.rule_button = tk.Button(self.root, text="Rules", width=10, height=2, command=self.show_rules)
        self.rule_button.grid(row=8, column=10, columnspan=2)
        self.root.resizable(False, False)

    def center_window(self, width, height):
        # Center the window on the screen

        self.width = width
        self.height = height

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position to center the window
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)

        # Set the window size and position
        self.root.geometry(f'{self.width}x{self.height}+{x}+{y}')   

    def create_grid(self) -> None:
        # Create a 9x9 grid of textboxes with black lines for 3x3 blocks
        for row in range(9):
            grid_row = []
            for col in range(9):
                # Create a frame to hold the entry widget and give it borders
                frame = tk.Frame(self.root, bd=2, relief='solid')  # Black border frame
                frame.grid(row=row, column=col, padx=(2 if col % 3 == 0 else 0, 2), pady=(2 if row % 3 == 0 else 0, 2))

                # Limit character input in each cell to 1 digit
                vcmd = (self.root.register(sud.limit_to_one_digit), '%P')

                # Create an entry widget inside the frame
                entry = tk.Entry(frame, width=2, justify='center', font=('Arial', 14), validate='key', validatecommand=vcmd)
                entry.pack(ipadx=5, ipady=5)  # Pack it into the frame
                entry.bind("<Enter>", lambda event, widget=entry: widget.config(bg="lightblue"))
                entry.bind("<Leave>", lambda event, widget=entry: widget.config(bg="white"))
                entry.config(cursor="arrow")
                grid_row.append(entry)
            self.grid.append(grid_row)

    def submit(self) -> None:
        # Handle the input submission, determine if the input board is solvable/unsolvable or invalid
        #self.sudoku_board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.grid[row][col].get()  # Get the value from the tk.Entry widget
                if value == '' or value == '0':
                    value = '0'  # Treat empty cells as 0
                else:
                    self.fixed_cells.add(str(row) + str(col))
                    self.grid[row][col].config(state='disabled', disabledbackground='lightblue', disabledforeground="black")
                current_row.append(int(value))  # Convert the value to an integer
            self.sudoku_board.append(current_row)

        # Print or process the submitted Sudoku board
        print("Submitted Sudoku Board:")
        sud.print_sudoku(self.sudoku_board)
        self.solvable, msg = sud.solve_sudoku(self.sudoku_board)
        
        self.submit_button['state'] = 'disable'
        self.generate_button['state'] = 'disable'
        
        if self.solvable:
            messagebox.showinfo("Board Submitted", "Board has been submitted!")
            self.solve_button['state'] = 'active'
            self.check_button['state'] = 'active'
        else:
            messagebox.showinfo("Board Not Submitted", "Input board is {}".format(msg))
            self.solve_button['state'] = 'disable'
            self.check_button['state'] = 'disable'

    def check_board(self) -> None:
        # Verify the user's solution based on the original input board
        user_board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.grid[row][col].get()  # Get the value from the tk.Entry widget
                if value == '' or value == '0':
                    value = '0'
                current_row.append(int(value))
            user_board.append(current_row)
        
        if sud.verify_sudoku(user_board):
            messagebox.showinfo("Congratulation", "Your solution to this board is correct!")
            self.check_button['state'] = 'disable'
            self.solve_button['state'] = 'disable'
        else:
            messagebox.showinfo("Unfortunately", "Your solution to this board is incorrect or incomplete.")

    def solve(self) -> None:
        # This function is only called when the board is determined solvable
        # The function will display the result on the GUI
        for row in range(9):
            for col in range(9):
                self.grid[row][col].delete(0, tk.END)
                self.grid[row][col].insert(0, str(self.sudoku_board[row][col]))
                if str(row) + str(col) in self.fixed_cells:
                    self.grid[row][col].config(state='disabled', disabledbackground='lightblue', disabledforeground="black")
                else:
                    self.grid[row][col].config(state='disabled', disabledbackground='white', disabledforeground="black")

        self.solve_button['state'] = 'disable'
        self.check_button['state'] = 'disable'

    def reset(self) -> None:
        # This function will reset the whole board, change all buttons' state to their original state
        for row in range(9):
            for col in range(9):
                self.grid[row][col].config(state='normal')
                self.grid[row][col].delete(0, tk.END)
                self.grid[row][col].config(bg='white')

        self.sudoku_board = []
        self.fixed_cells = set()
        self.solvable = False
        self.solve_button['state'] = 'disable'
        self.submit_button['state'] = 'active'
        self.check_button['state'] = 'disable'
        self.generate_button['state'] = 'active'

    def generate(self):
        message_box = Toplevel(root)
        message_box.title("Difficulty")
        message_box.geometry("230x35") 
       # Center the message box relative to the parent window (root)
        message_box.update_idletasks()
        parent_x = root.winfo_x()
        parent_y = root.winfo_y()
        parent_width = root.winfo_width()
        parent_height = root.winfo_height()

        # Calculate the position to center the message box relative to the parent window
        x_cordinate = parent_x + (parent_width // 2) - (300 // 2)  # Fixed width of 300
        y_cordinate = parent_y + (parent_height // 2) - (150 // 2)  # Fixed height of 150

        # Set the position of the message box
        message_box.geometry(f"+{x_cordinate}+{y_cordinate}")

        # Add buttons to the message box
        button1 = tk.Button(message_box, text="EASY", command=lambda: close_message_box("EASY"))
        button1.grid(row=1, column=1, padx=5)

        button2 = tk.Button(message_box, text="MEDIUM", command=lambda: close_message_box("MEDIUM"))
        button2.grid(row=1, column=2, padx=5)

        button3 = tk.Button(message_box, text="HARD", command=lambda: close_message_box("HARD"))
        button3.grid(row=1, column=3, padx=5)

        button4 = tk.Button(message_box, text="EXPERT", command=lambda: close_message_box("EXPERT"))
        button4.grid(row=1, column=4, padx=5)

        def close_message_box(mode):
            self.difficulty = mode
            message_box.destroy()
            temp = []
            #print(f"Difficulty {mode} was selected")
            while not self.solvable:
                temp = sud.spawn(self.difficulty)
                sud.print_sudoku(temp)
                self.sudoku_board = copy.deepcopy(temp)
                self.solvable, msg = sud.solve_sudoku(temp)

            for row in range(9):
                for col in range(9):
                    if self.sudoku_board[row][col] != 0:
                        self.fixed_cells.add(str(row) + str(col))
                        self.grid[row][col].delete(0, tk.END)
                        self.grid[row][col].insert(0, str(self.sudoku_board[row][col]))
                        self.grid[row][col].config(state='disabled', disabledbackground='lightblue', disabledforeground="black")

            self.sudoku_board = temp
            self.generate_button['state'] = 'disable'
            self.submit_button['state'] = 'disable'
            self.solve_button['state'] = 'active'
            self.check_button['state'] = 'active'

    def show_rules(self) -> None:
        rule1 = "Rule 1: Each row must contain the numbers from 1 to 9, without repetitions"
        rule2 = "Rule 2: Each column must contain the numbers from 1 to 9, without repetitions"
        rule3 = "Rule 3: The digits can only occur once per block (3x3)"
        messagebox.showinfo("Rules", f'{rule1}\n{rule2}\n{rule3}')
    
if __name__ == "__main__":
    root = tk.Tk()
    #app = CenteredWindow(root, width=475, height=390)
    gui = SudokuGUI(root, width=475, height=390)
    root.mainloop()
