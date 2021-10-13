import random

# This algorithm generates a maze with the depth-first search approach, 
# meaning that a path is explored as long as possible, only backtracking if 
# there is no way forward anymore. How this basically works is that, starting 
# from a random node, each of the adjacent cells represents a wall and only 
# the node which is two steps away represents a neighbor. And eacht time the
# algorithm moves from the current node to a neighbor, the wall in-between 
# those nodes is torn down. At the end of the process each node has been 
# visited but, of course, not all walls have been destroyed, leaving behind 
# the maze.

class Maze_node :
    def __init__(self, row, col, wall) :
        self.row = row
        self.col = col
        self.wall = wall
        self.visited = False

def make_maze(height, width) :
    grid = []
    for i in range(height) :
        row = []
        for j in range(width) :
            row.append(Maze_node(i, j, True))
        grid.append(row)

    # The stack (which is just a list here) keeps track of which nodes are 
    # still to be evaluated
    stack = []

    # A random node gets assigned to the current node variable
    current_node = grid[random.randint(0, height - 1)][random.randint(0, width - 1)]

    while True :

        # The current nodes is pushed onto the stack, gets marked as visited 
        # and the wall which it currently holds in itself has to be destroyed 
        # (because in the grid every node starts marked as a wall)
        stack.append(current_node)
        current_node.visited = True
        current_node.wall = False

        # The neighbors of the current node (nodes that are two steps away in 
        # the top, bottom, left and right direction from the node) are fetched
        neighbors = get_neighbors(current_node, grid)

        # If there are no unvisited neighbors for the current node, the 
        # current node is removed from the stack, if the stack then is empty,
        # the process if finished, if not, the node on top of the stack will 
        # become the new current node (it is popped here because the current 
        # node is always pushed onto the stack at the beginning of the loop 
        # and we do not want it there twice)
        if len(neighbors) == 0 :
            stack.pop(len(stack) - 1)
            if len(stack) == 0 :
                break
            current_node = stack.pop(len(stack) - 1)
            continue

        # If there are unvisited nodes adjacent to the current node, one is 
        # randomly picked and the wall between the current node and the chosen 
        # neighboring node torn down; the neighbor then becomes the new 
        # current node
        else :
            neighbor = random.choice(neighbors)
            wall_between = get_wall(current_node, neighbor, grid)
            wall_between.wall = False
            current_node = neighbor

    return grid

def get_neighbors(node, grid) :
    neighbors = []
    row = node.row
    col = node.col

    if row - 2 >= 0 and not grid[row - 2][col].visited : neighbors.append(grid[row - 2][col])
    if col -2 >= 0 and not grid[row][col - 2].visited : neighbors.append(grid[row][col - 2])
    if row + 2 < len(grid) and not grid[row + 2][col].visited : neighbors.append(grid[row + 2][col])
    if col + 2 < len(grid[0]) and not grid[row][col + 2].visited : neighbors.append(grid[row][col + 2])

    return neighbors

def get_wall(node, neighbor, grid) :
    if node.row == neighbor.row :
        row = node.row
        col = max(node.col, neighbor.col) - 1
    else :
        col = node.col
        row = max(node.row, neighbor.row) - 1

    return grid[row][col]

