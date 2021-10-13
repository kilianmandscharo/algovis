# The dijkstra-algorithm finds the shortest path in a graph from one node to 
# another. In this case the graph is a grid, with the weights being initially 
# set to 1, meaning that a node can be reached from the top-, bottom-, left- 
# and right-side neighbor with a cost of 1. Dijkstra always finds the optimal 
# solution, if a solution exists.

class Node :
    def __init__(self, row, col, wall, weight) :
        self.row = row
        self.col = col
        self.distance = float('inf')
        self.predecessor = None
        self.wall = wall
        self.weight = weight

def dijkstra(input_grid, start_row, start_col, dest_row, dest_col) :

    # Grid is copied and new Nodes are made, when I did not do that there was 
    # a bug, where some of the walls seemingly were not recognized anymore by 
    # the algorithm
    grid = []
    for i in range(len(input_grid)) :
        row = []
        for j in range(len(input_grid[0])) :
            node = input_grid[i][j]
            new_node = Node(node.row, node.col, node.wall, node.weight)
            row.append(new_node)
        grid.append(row)

    # The distance of the start node is set to 0, which means that the start 
    # node is the first node to be evaluated
    grid[start_row][start_col].distance = 0

    # All nodes from the grid are put into a list
    unvisited = get_nodes(grid)

    # This list will be returned at the end and contains all nodes in the 
    # order that they were visited
    visited = []

    while unvisited :

        # The list is sorted and the node with the lowest distance in the next 
        # step removed from the list, stored as the current node and appended 
        # to the visited nodes
        unvisited.sort(key=lambda x : x.distance)
        current_node = unvisited.pop(0)
        visited.append(current_node)

        # If the current node is the destination node, the algorithm returns; 
        # if the distance of the current node is infinity, meaning no
        # node can be further reached, it also returns
        if (current_node.row == dest_row and current_node.col == dest_col) or current_node.distance == float('inf') :
            return visited

        # All neighbor nodes of the current node are gathered and if they are 
        # not a wall, the distance of the current node plus the weight of each 
        # of the neighbor nodes are compared with the distance of the 
        # respecitve neighbor; if the new distance is shorter, the distance of 
        # the neighbor gets updated as well as its predecessor
        neighbors = get_neighbors(grid, current_node)
        for neighbor in neighbors :
            if neighbor.wall :
                continue
            else :
                if current_node.distance + neighbor.weight < neighbor.distance :
                    neighbor.distance = current_node.distance + neighbor.weight
                    neighbor.predecessor = current_node

def get_neighbors(grid, node) :
    row = node.row
    col = node.col
    reVal = []
    if row - 1 >= 0 : reVal.append(grid[row-1][col])
    if row + 1 < len(grid) : reVal.append(grid[row+1][col])
    if col - 1 >= 0 : reVal.append(grid[row][col-1])
    if col + 1 < len(grid[0]) : reVal.append(grid[row][col+1])
    return reVal

def get_nodes(grid) :
    reVal = []
    for i in range(len(grid)) :
        for j in range(len(grid[0])) :
            reVal.append(grid[i][j])
    return reVal
