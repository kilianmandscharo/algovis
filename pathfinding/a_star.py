# The A* algorithm knows, in constrast to Dijkstra's algorithm, where the 
# destination node is. That is, each node has a g value, the equivalent to the 
# distance attribute of the Dijkstra nodes, an h value, which is the absolute 
# distance from this node to the destination, and an f value, which is the 
# overall cost of the node, calculated by adding g and h value. A* also will 
# find the optimal solution, if a solution exists

from dijkstra import get_neighbors

# Definition of the new node, which is used in the algorithm
class A_star_node :
    def __init__(self, row, col, h, wall, weight) :
        self.row = row
        self.col = col
        self.h = h
        self.g = float('inf')
        self.f = float('inf')
        self.wall = wall
        self.weight = weight
        self.predecessor = None

def a_star(input_grid, start_row, start_col, dest_row, dest_col) :

    # A new grid is made, with all the relevant information of each node given 
    # to the new A* nodes
    grid = []
    for i in range(len(input_grid)) :
        new_row = []
        for j in range(len(input_grid[0])) :
            node = input_grid[i][j]
            new_row.append(A_star_node(node.row, node.col, abs(node.row - dest_row) + abs(node.col - dest_col), node.wall, node.weight))
        grid.append(new_row)

    # Each node that is evaluated as the neighbor of the current node is put 
    # into the open list, each node that is evaluated as the current node is 
    # put into the closed list
    open_list = []
    closed_list = []

    # The start node gets a g value of 0 and is put into the open list to be 
    # evaluated first
    start_node = grid[start_row][start_col]
    start_node.g = 0
    open_list.append(start_node)

    # Here again the list of nodes which gets returned and animated
    visited = []

    while open_list :

        # The open list is sorted by the f value of the nodes, the node with 
        # the lowest f value gets to be the current node and is put into the 
        # closed list as well as appended to the visited nodes for the later 
        # animation of the search
        open_list.sort(key=lambda x : x.f)
        current_node = open_list.pop(0)
        closed_list.append(current_node)
        visited.append(current_node)

        # If the current node ist the destination node or if the current node 
        # is unreachable the funtion returns the visited nodes
        if (current_node.row == dest_row and current_node.col == dest_col) or current_node.g == float('inf') :
            return visited

        # Take the neighbors of the current node to evaluate them if they are 
        # not a wall and not in the closed list
        neighbors = get_neighbors(grid, current_node)
        for neighbor in neighbors :
            if check_if_node_in_list(neighbor, closed_list) or neighbor.wall :
                continue
            else :

                # If the neighbor is not in the open list or if the new path 
                # to the neighbor is shorter, the g and consequently f value
                # are updated and the current node gets to be the new 
                # predecessor of the neighbor; the neighbor also is appended 
                # to the open list if it is not already a member
                new_g = current_node.g + neighbor.weight
                if not check_if_node_in_list(neighbor, open_list) or new_g < neighbor.g :
                    neighbor.g = new_g
                    neighbor.f = new_g + neighbor.h
                    neighbor.predecessor = current_node
                    if not check_if_node_in_list(neighbor, open_list):
                        open_list.append(neighbor)
    return visited

def check_if_node_in_list(current_node, l) :
    for node in l :
        if current_node.row == node.row and current_node.col == node.col :
            return True
    return False

