import tkinter as tk
from tkinter import font as f
import time
from dijkstra import dijkstra
from dijkstra import Node
from a_star import a_star
from maze import make_maze

#============================================================================#
# Color variables
START_COLOR = "#63A46C"
DEST_COLOR = "#BD1E1E"
WALL_COLOR = "black"
WEIGHT_COLOR = "#af6ccc"
VISITED_COLOR = "#82DDF0"
PATH_COLOR = "orange"
NODE_COLOR = "white"
BUTTON_COLOR = "#517096"

# Initialize GUI
root = tk.Tk()

#============================================================================#
# Class that holds the state of the pathfinder application
class Pathfinder :
    def __init__(self) :
        self.running = False
        self.algorithm = tk.StringVar(root, "Dijkstra")
        self.obstacle = tk.StringVar(root, "Wall")

pathfinder = Pathfinder()

#============================================================================#
# Main grid that holds important variables and the grid itself
class Grid :
    def __init__(self) :
        self.width = 49
        self.height = 29
        self.start_row = 15
        self.start_col = 2
        self.dest_row = 15
        self.dest_col = 46
        self.dragging = False
        self.start_dragging = False
        self.dest_dragging = False
        self.grid = self.make_grid(self.height, self.width)

    def make_grid(self, height, width) :
        grid = []
        for i in range(height) :
            new_row = []
            for j in range(width) :
                node = Node(i, j, False, 1)
                new_row.append(node)
            grid.append(new_row)
        return grid

# Create instance of Grid
grid = Grid()

#============================================================================#
# Function that receives the nodes that were visited during the execution of 
# the pathfinding algorithm and animates the search process
def animate_pathfinding() :
    if pathfinder.algorithm.get() == "Dijkstra" :
        nodes = dijkstra(grid.grid, grid.start_row, grid.start_col, grid.dest_row, grid.dest_col)
    else :
        nodes = a_star(grid.grid, grid.start_row, grid.start_col, grid.dest_row, grid.dest_col)
    if nodes :
        for node in nodes :
            if (node.row == grid.start_row and node.col == grid.start_col) or (node.row == grid.dest_row and node.col == grid.dest_col) :
                continue
            if grid.grid[node.row][node.col].weight == 1 :
                label_grid[node.row][node.col].configure(background=VISITED_COLOR)
            root.update()
        last_node = nodes[-1]

        # Only if the last visited node is the destination node the path from 
        # start to destinaiton is animated
        if last_node.row == grid.dest_row and last_node.col == grid.dest_col :
            path = get_path(last_node)
            animate_shortest_path(path)

# Function that receives the nodes that make up the shortest path from start 
# to destination and animates it
def animate_shortest_path(path) :
    for node in path :
        if (node.row == grid.start_row and node.col == grid.start_col) or (node.row == grid.dest_row and node.col == grid.dest_col) :
            continue
        label_grid[node.row][node.col].configure(background=PATH_COLOR)
        time.sleep(0.01)
        root.update()

# Receives the final node of the sucessful search process and goes back to the 
# start through the respective predecessor
def get_path(node) :
    reVal = []
    while node.predecessor :
        node = node.predecessor
        reVal.insert(0, node)
    return reVal

#=================================================================#
# Function that handles if the mouse cursor moves into a node while either one 
# of the dragging actions is active
def update_grid(event) :

    if pathfinder.running :
        return

    # Each node is placed in a frame which is then placed into the grid, to 
    # make forming the nodes as squares easier; this means, however, that to 
    # get the row and column a node is in, we need the parent frame of the 
    # node, which happens here
    node = event.widget
    parent_name = node.winfo_parent()
    parent = root._nametowidget(parent_name)
    row = parent.grid_info()["row"]
    col = parent.grid_info()["column"]

    # If dragging is active, either a wall or a weight is placed, depending on 
    # what is selected
    if grid.dragging :
        if pathfinder.obstacle.get() == "Wall" :
            if (row == grid.start_row and col == grid.start_col) or (row == grid.dest_row and col == grid.dest_col) :
                return
            wall = grid.grid[row][col].wall
            grid.grid[row][col].wall = not wall
            node.configure(background=NODE_COLOR if wall else WALL_COLOR)
        else :
            if (row == grid.start_row and col == grid.start_col) or (row == grid.dest_row and col == grid.dest_col) or grid.grid[row][col].wall :
                return
            weight = grid.grid[row][col].weight
            grid.grid[row][col].weight = 1 if weight > 1 else 3
            node.configure(background=NODE_COLOR if weight > 1 else WEIGHT_COLOR)

    # If start dragging is active, the starting node gets moved around the 
    # grid; both the grid of the Grid class as well as the grid, which 
    # contains the graphic elements have to be updated of course
    elif grid.start_dragging :
        if (row == grid.dest_row and col == grid.dest_col) or grid.grid[row][col].wall :
            return
        else :
            label_grid[grid.start_row][grid.start_col].configure(background=NODE_COLOR)
            label_grid[row][col].configure(background=START_COLOR)
            grid.start_row = row
            grid.start_col = col

    # The same concept with the destination node
    elif grid.dest_dragging :
        if (row == grid.start_row and col == grid.start_col) or grid.grid[row][col].wall :
            return
        else :
            label_grid[grid.dest_row][grid.dest_col].configure(background=NODE_COLOR)
            label_grid[row][col].configure(background=DEST_COLOR)
            grid.dest_row = row
            grid.dest_col = col

# Determines which kind of dragging is activated when the mouse is clicked, 
# depending on where the click happens
def set_dragging(event) :
    if pathfinder.running :
        return
    node = event.widget
    parent_name = node.winfo_parent()
    parent = root._nametowidget(parent_name)
    row = parent.grid_info()["row"]
    col = parent.grid_info()["column"]
    if row == grid.start_row and col == grid.start_col :
        grid.start_dragging = not grid.start_dragging
    elif row == grid.dest_row and col == grid.dest_col :
        grid.dest_dragging = not grid.dest_dragging
    else :
        grid.dragging = not grid.dragging

#=================================================================#
# The functions in this section handle all the buttons that can be clicked
def on_click_start() :
    if pathfinder.running :
        return
    for i in range(grid.height) :
        for j in range(grid.width) :
            node = grid.grid[i][j]
            if node.wall or node.weight > 1 or (node.row == grid.start_row and node.col == grid.start_col) or (node.row == grid.dest_row and node.col == grid.dest_col) :
                continue
            else :
                label_grid[i][j].configure(background=NODE_COLOR)

    pathfinder.running = True
    animate_pathfinding()
    pathfinder.running = False

def on_click_reset() :
    if pathfinder.running :
        return
    for i in range(grid.height) :
        for j in range(grid.width) :
            node = grid.grid[i][j]
            node.weight = 1
            node.wall = False
            if (i == grid.start_row and j == grid.start_col) or (i == grid.dest_row and j == grid.dest_col) :
                continue
            else :
                label_grid[i][j].configure(background=NODE_COLOR)

def on_click_obstacle() :
    if pathfinder.running :
        return
    pathfinder.obstacle.set("Wall" if pathfinder.obstacle.get() == "Weight" else "Weight")

def on_click_algorithm() :
    if pathfinder.running :
        return
    pathfinder.algorithm.set("A*" if pathfinder.algorithm.get() == "Dijkstra" else "Dijkstra")

def on_click_maze() :
    if pathfinder.running :
        return
    for row in grid.grid :
        for node in row :
            node.wall = False
            node.weight = 1
            label_grid[node.row][node.col].configure(background=NODE_COLOR)
    maze = make_maze(grid.height, grid.width)
    for row in maze :
        for node in row :
            if node.wall :
                grid.grid[node.row][node.col].wall = True
                label_grid[node.row][node.col].configure(background=WALL_COLOR)
    i = 0
    while True :
        if grid.grid[15][i].wall :
            i += 1
        else :
            break
    grid.start_row = 15
    grid.start_col = i
    label_grid[15][i].configure(background=START_COLOR)

    j = grid.width - 1
    while True :
        if grid.grid[15][j].wall :
            j -= 1
        else :
            break
    grid.dest_row = 15
    grid.dest_col = j
    label_grid[15][j].configure(background=DEST_COLOR)

#============================================================================#
# Building the GUI
root.geometry("900x650")

button_font = f.Font(family="Futura", size=20)

grid_frame = tk.Frame(root, highlightbackground="black", highlightthickness=3)
grid_frame.pack(pady=10)

# Label grid is constructed
label_grid = [[0 for i in range(grid.width)] for i in range(grid.height)]

for i in range(grid.height) :
    for j in range(grid.width) :
        container = tk.Frame(grid_frame, width=15, height=15)
        node = tk.Label(container, background="white", borderwidth=1, relief="solid")
        container.grid_propagate(False)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.grid(row = i, column = j)
        node.grid(sticky="wens")
        node.bind("<Enter>", update_grid)
        node.bind("<Button-1>", set_dragging)
        label_grid[i][j] = node

# Start and destination are marked on the GUI grid
label_grid[grid.start_row][grid.start_col].configure(background=START_COLOR)
label_grid[grid.dest_row][grid.dest_col].configure(background=DEST_COLOR)

# Buttons
button_section_1 = tk.Frame(root)
button_section_1.pack(pady=5)

start_button = tk.Button(button_section_1, text="Start", command=on_click_start, font=button_font, fg=BUTTON_COLOR)
start_button.pack(side="left", padx=10)

reset_button = tk.Button(button_section_1, text="Reset", command=on_click_reset, font=button_font, fg=BUTTON_COLOR)
reset_button.pack(side="left", padx=10)

maze_button = tk.Button(button_section_1, text="Maze", command=on_click_maze, font=button_font, fg=BUTTON_COLOR)
maze_button.pack(side="left", padx=10)

button_section_2 = tk.Frame(root)
button_section_2.pack(pady=5)

obstacle_label = tk.Label(button_section_2, textvariable=pathfinder.obstacle, font=button_font)
obstacle_label.pack(side="right")

obstacle_button = tk.Button(button_section_2, text="Change obstacle:", command=on_click_obstacle, font=button_font, fg=BUTTON_COLOR)
obstacle_button.pack(side="right", padx=10)

algorithm_label = tk.Label(button_section_2, textvariable=pathfinder.algorithm, font=button_font)
algorithm_label.pack(side="right")

algorithm_button = tk.Button(button_section_2, text="Change algorithm:", command=on_click_algorithm, font=button_font, fg=BUTTON_COLOR)
algorithm_button.pack(side="right", padx=10)

# Legend
legend_section = tk.Frame(root, highlightbackground="black", highlightthickness=1)
legend_section.pack(pady=5)

start_label = tk.Label(legend_section, text="Start =")
start_label.pack(side="left", padx=5)

start_square = tk.Label(legend_section, height=1, width=2, background=START_COLOR)
start_square.pack(side="left", padx=5)

dest_label = tk.Label(legend_section, text="Destination =")
dest_label.pack(side="left", padx=5)

dest_square = tk.Label(legend_section, height=1, width=2, background=DEST_COLOR)
dest_square.pack(side="left", padx=5)

wall_label = tk.Label(legend_section, text="Wall =")
wall_label.pack(side="left", padx=5)

wall_square = tk.Label(legend_section, height=1, width=2, background=WALL_COLOR)
wall_square.pack(side="left", padx=5)

weight_label = tk.Label(legend_section, text="Weight =")
weight_label.pack(side="left", padx=5)

weight_square = tk.Label(legend_section, height=1, width=2, background=WEIGHT_COLOR)
weight_square.pack(side="left", padx=5)

path_label = tk.Label(legend_section, text="Path =")
path_label.pack(side="left", padx=5)

path_square = tk.Label(legend_section, height=1, width=2, background=PATH_COLOR)
path_square.pack(side="left", padx=5)

visited_label = tk.Label(legend_section, text="Visited =")
visited_label.pack(side="left", padx=5)

visited_square = tk.Label(legend_section, height=1, width=2, background=VISITED_COLOR)
visited_square.pack(side="left", padx=5)

# Instruction
explanation_section = tk.Frame(root)
explanation_section.pack(pady=5)

explanation_1 = tk.Label(explanation_section, text="To move the start or destination, click on the respective square, release the mouse, re-position the square and click again.")
explanation_1.pack()

explanation_2 = tk.Label(explanation_section, text="To draw a wall-section or a section of weights, click on an empty node, release the mouse, draw the obstacle and then click again.")
explanation_2.pack()

root.mainloop()
