import numpy as np
import tkinter as tk
from tkinter import font as f
import copy

root = tk.Tk()

#============================================================================#
# Class that holds the sudoku and the important functions for solving it
class Solver :
    def __init__(self) :

        # Actually there are two representations of the same sudoku, so to
        # say, once in this form as a 2d-list of numbers, and once as a 2d-
        # list full of tkinter variables, that are connected directly to the
        # entries of the GUI, the reason being that it is much easier to work
        # with the numbers of the former while the latter is necessary to
        # continue updating the numbers in the GUI
        self.sudoku = [[0, 0, 0,  7, 1, 0,  0, 0, 0],
                       [7, 0, 2,  6, 0, 8,  4, 0, 0],
                       [0, 0, 0,  0, 0, 2,  1, 0, 7],

                       [0, 0, 0,  0, 3, 6,  0, 0, 0],
                       [0, 0, 6,  0, 2, 0,  0, 5, 0],
                       [3, 0, 0,  0, 8, 4,  2, 0, 1],

                       [0, 0, 0,  3, 0, 0,  8, 0, 2],
                       [4, 0, 3,  8, 7, 0,  6, 0, 0],
                       [0, 0, 8,  2, 0, 0,  0, 0, 3]]

        self.tk_sudoku = self.make_tk_sudoku()

        # Temporary copy of the sudoku to be able to reset to this copy
        self.temp = copy.deepcopy(self.sudoku)

        # Indicates if the solving process is running, disabling the buttons
        # during the process
        self.running = False

    # Create the 2d-list that holds the tkinter variable objects
    def make_tk_sudoku(self) :
        tk_sudoku = [[0 for i in range(9)] for j in range(9)]
        for i in range(9) :
            for j in range(9) :
                var = tk.StringVar()
                var.set(self.sudoku[i][j] if self.sudoku[i][j] != 0 else "")
                tk_sudoku[i][j] = var
        return tk_sudoku

    # Gets the next cell that is empty during the solving process
    def get_next_cell(self, board) :
        for i in range(9) :
            for j in range(9) :
                if board[i][j] == 0 :
                    return i, j
        return None, None

    # Tests whether a certain number in a certain location in the sudoku
    # clashes with the same number in the same row, diagonal or block
    def test_input (self, y, x, number, board) :
        #Horizontal
        if number in board[y] :
            return False

        #Vertical
        vert_arr = []
        for i in range(9) :
            vert_arr.append(board[i][x])

        if number in vert_arr :
            return False

        #Blocks
        block_arr = []
        xDir = (x // 3) * 3
        yDir = (y // 3) * 3
        for i in range(3) :
            for j in range(3) :
                block_arr.append(board[i + yDir][j + xDir])

        if number in block_arr :
            return False

        return True

    # Function for recursively solving the sudoku with backtracking which
    # essentially means the functions go down the tree of possible
    # combinations as far as possible, backtracking if there is no further
    # number to be successfully placed to a node in the tree, from where
    # another path down the tree is possible; if one solution is found, the
    # process returns
    def solve_sudoku(self) :
        row, col = self.get_next_cell(self.sudoku)

        if row is None :
            return True

        for num in range(1, 10) :
            if self.test_input(row, col, num, self.sudoku) :

                # Here three 2d-lists are essentially handled at the same
                # time, first the sudoku with numbers, that gets evaluated in
                # the test_input function, second the sudoku with tkinter
                # objects, which updates the numbers in the GUI, and thirdly
                # the list of entries, that handles the colors of the GUI
                self.sudoku[row][col] = num
                self.tk_sudoku[row][col].set(num)
                entries[row][col].configure({"bg": "#59CD90"})
                root.update()
                if self.solve_sudoku() :
                    return True

            # If the function reaches this part that means that none of the
            # lower paths were successful in solving the sudoku and the
            # current number is set to 0, false is returned, when none of the
            # numers branch into a solution
            self.sudoku[row][col] = 0
            self.tk_sudoku[row][col].set("")
            entries[row][col].configure({"bg": "#EE6352"})
        return False

    # Function to test whether anywhere on the board there is an illegal
    # combination of numbers, in case returning every row, col or block where
    # such numbers are located
    def valid_board(self, board):
        reval = []
        def array_tester(arr) :
            for num in arr :
                if num != 0 and arr.count(num) > 1 :
                    return False
            return True

        # Block
        for x in range(0, 7, 3) :
            for i in range(0, 7, 3) :
                block = []
                for j in range(3) :
                    for k in range(0 + x, 3 + x) :
                        block.append(board[j + i][k])
                if not array_tester(block) :
                    reval.append(["block", i, x])
        # Vertical
        for i in range(9) :
            col = []
            for j in range(9) :
                col.append(board[j][i])
            if not array_tester(col) :
                reval.append(["col", i])

        # Horizontal
        for i, row in enumerate(board) :
            if not array_tester(row) :
                reval.append(["row", i])

        return reval

    # Tests if the entries entered by the user are legal
    def entries_test(self) :
        for i in range(9) :
            for j in range(9) :
                val = self.tk_sudoku[i][j].get()
                if val == "" :
                    continue
                if val.isdigit() :
                    val = int(val)
                    if val < 1 or val > 9 :
                        print("Only enter nubmers between 1-9.")
                        return False
                else :
                    print("Only enter numbers between 1-9.")
                    return False
        return True

# Create instance of the solver
solver = Solver()

#============================================================================#
# On click functions

# Function that is bound to the solve button; if all of the entries are legal
# the entries are copied to the sudoku that only holds numbers, so that the
# values in this sudoku and the one that holds the tkinter variables are
# identical for the solving process
def on_click_solve() :
    if solver.running :
        return
    if solver.entries_test() :
        for i in range(9) :
            for j in range(9) :
                val = solver.tk_sudoku[i][j].get()
                val = 0 if val == "" else int(val)
                solver.sudoku[i][j] = val

        # Any invalid sections are returned by the valid_board function, if none are found the solving process begins
        invalid_sections = solver.valid_board(solver.sudoku)
        if len(invalid_sections) == 0 :
            print("Solving...")
            solver.temp = copy.deepcopy(solver.sudoku)
            solver.running = True
            solved = solver.solve_sudoku()
            print("Solved" if solved else "Not solved")
            print(np.matrix(solver.sudoku))
            solver.running = False

        # In case of any invalid number combinations each row, column or block that holds illegal numbers is marked in red
        else :
            print("Invalid board")
            for entry in invalid_sections :
                if entry[0] == "row" :
                    for i in range(9) :
                        entries[entry[1]][i].configure(background="#EE6352")
                elif entry[0] == "col" :
                    for i in range(9) :
                        entries[i][entry[1]].configure(background="#EE6352")
                else :
                    for i in range(3) :
                        for j in range(3) :
                            entries[i + entry[1]][j + entry[2]].configure(background="#EE6352")

# Clears the sudoku so that all entries are empty
def on_click_clear() :
    if solver.running :
        return
    for i in range(9) :
        for j in range(9) :
            solver.tk_sudoku[i][j].set("")
            solver.sudoku[i][j] = 0
            entries[i][j].configure({"bg":"white"})

    print("Cleared")

# Resets to the last sudoku saved in the temp sudoku in the solver
def on_click_reset() :
    if solver.running :
        return
    solver.sudoku = copy.deepcopy(solver.temp)
    for i in range(9) :
        for j in range(9) :
            val = solver.sudoku[i][j]
            solver.tk_sudoku[i][j].set(val if val > 0 else "")
            entries[i][j].configure({"bg":"white"})
    print("Reset")

# Appends the current sudoku shown in the GUI to a textfile
def on_click_save() :
    if solver.running :
        return
    with open("sudoku.txt", "a") as h :
        s = solver.sudoku
        for i, row in enumerate(s) :
            if i % 3 == 0 :
                h.write("\n")
            for j, num in enumerate(row) :
                if j % 3 == 0 :
                    h.write(f" {str(num)}")
                else :
                    h.write(str(num))
            h.write("\n")
        h.write("=====================")
    print("Sudoku saved!")

# ===========================================================================#
# Layout

root.geometry("500x535")

top_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2)
top_frame.pack(pady=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

# The grid is separated into nine blocks, so that every block can have its own
# border, making the sudoku visually clearer
frame1 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame1.grid(row=0, column=0)
frame2 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame2.grid(row=0, column=1)
frame3 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame3.grid(row=0, column=2)
frame4 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame4.grid(row=1, column=0)
frame5 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame5.grid(row=1, column=1)
frame6 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame6.grid(row=1, column=2)
frame7 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame7.grid(row=2, column=0)
frame8 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame8.grid(row=2, column=1)
frame9 = tk.Frame(top_frame, highlightbackground="black", highlightthickness=2)
frame9.grid(row=2, column=2)

button_font = f.Font(family="Futura", size=25)

solve_button = tk.Button(bottom_frame, text="Solve", fg="#59CD90", command=on_click_solve, font=button_font, padx=5, pady=5)
solve_button.pack(side="left", padx=10)
save_button = tk.Button(bottom_frame, text="Save", fg="#3FA7D6", command=on_click_save, font=button_font, padx=5, pady=5)
save_button.pack(side="right", padx=10)
reset_button = tk.Button(bottom_frame, text="Reset", fg="#FAC05E", command=on_click_reset, font=button_font, padx=5, pady=5)
reset_button.pack(side="right", padx=10)
clear_button = tk.Button(bottom_frame, text="Clear", fg="#EE6352", command=on_click_clear, font=button_font, padx=5, pady=5)
clear_button.pack(side="right", padx=10)

# The entries are placed in the nine frames and put into the entries 2d list
# that gets updated in the solving process to change the colors accordingly
entries = [[0 for i in range(9)] for j in range(9)]

for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame1, textvariable=solver.tk_sudoku[i][j], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i][j] = e
for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame2, textvariable=solver.tk_sudoku[i][j+3], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i][j+3] = e
for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame3, textvariable=solver.tk_sudoku[i][j+6], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i][j+6] = e
for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame4, textvariable=solver.tk_sudoku[i+3][j], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i+3][j] = e
for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame5, textvariable=solver.tk_sudoku[i+3][j+3], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i+3][j+3] = e
for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame6, textvariable=solver.tk_sudoku[i+3][j+6], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i+3][j+6] = e
for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame7, textvariable=solver.tk_sudoku[i+6][j], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i+6][j] = e
for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame8, textvariable=solver.tk_sudoku[i+6][j+3], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i+6][j+3] = e
for i in range(3) :
    for j in range(3) :
        e = tk.Entry(frame9, textvariable=solver.tk_sudoku[i+6][j+6], width=4, borderwidth=1, relief="solid", justify="center")
        e.grid(row=i, column=j, ipady=10)
        entries[i+6][j+6] = e

root.mainloop()
