# Somehow running the project does not work in Spyder

import tkinter as tk
import os
from tkinter import font as f
from PIL import ImageTk, Image

root = tk.Tk()
root.geometry("500x400")

# Functions to open the two applications respectively

def open_pathfinder() :
    process = os.popen("python3 pathfinding/pathfinding.py", "w")
    process.close()

def open_sudoku() :
    process = os.popen("python3 sudoku/sudoku.py", "w")
    process.close()


#============================================================================#
# Fonts
header_1_font = f.Font(family="Futura", size=25)
header_2_font = f.Font(family="Lobster 1.3", size=50)
button_font = f.Font(family="Futura", size=30)

#============================================================================#
# Layout
header_section = tk.Frame(root)
header_section.pack(pady=40)

arrow_section = tk.Frame(root)
arrow_section.pack()

button_section = tk.Frame(root)
button_section.pack(pady=40)

header_1 = tk.Label(header_section, text="Welcome to", font=header_1_font)
header_1.pack()

header_2 = tk.Label(header_section, text="Visualizing Algorithms", font=header_2_font, fg="#6cbbcc")
header_2.pack()

image_1 = Image.open("images/arrow.png")
image_2 = Image.open("images/arrow.png")
image_1 = image_1.resize((50, 50), Image.ANTIALIAS)
image_2 = image_2.resize((50, 50), Image.ANTIALIAS)
arrow_1 = ImageTk.PhotoImage(image_1)
arrow_2 = ImageTk.PhotoImage(image_2)

i_1_label = tk.Label(arrow_section, image=arrow_1)
i_1_label.pack(side="left", padx=85)
i_2_label = tk.Label(arrow_section, image=arrow_2)
i_2_label.pack(side="right", padx=85)

s_button_frame = tk.Frame(button_section, highlightbackground="#af6ccc", highlightthickness=4, width=210, height=60)
s_button_frame.grid_propagate(False)
s_button_frame.columnconfigure(0, weight=1)
s_button_frame.rowconfigure(0, weight=1)
s_button_frame.pack(side="left", padx=10)

p_button_frame = tk.Frame(button_section, highlightbackground="#af6ccc", highlightthickness=4, width=210, height=60)
p_button_frame.grid_propagate(False)
p_button_frame.columnconfigure(0, weight=1)
p_button_frame.rowconfigure(0, weight=1)
p_button_frame.pack(side="right", padx=10)

button_path = tk.Button(p_button_frame, text="Pathfinder", command=open_pathfinder, font=button_font)
button_path.grid(sticky="wens")

button_sudoku = tk.Button(s_button_frame, text="Sudoku-solver", command=open_sudoku, font=button_font)
button_sudoku.grid(sticky="wens")

root.mainloop()
