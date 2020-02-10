import math


# main method for A*(informed search), which will take the index of start point(str),the index of end point(str),
# and the nodes map(dict)
def a_star(start_index, goal_index, nodes):
    close_list = {}  # list for nodes which have already evaluated
    open_list = {}  # list for noes which need to be evaluated
    came_from = {}  # dict for recording the moves
    start_node = nodes[start_index]
    start_node.g = 0
    start_node.h = heuristic(start_node.index, goal_index, nodes)
    start_node.f = start_node.g + start_node.h
    open_list[start_node] = 1
    while open_list:
        current_node = get_lowest_f(open_list)
        del open_list[current_node]
        close_list[current_node] = 1
        # arrive the goal node, stop searching
        if current_node.index == goal_index:
            return current_node.g
        neighbors = get_neighbors(current_node, nodes)
        for neighbor in neighbors:
            # ignore the neighbor which is the parent
            if neighbor in close_list.keys():
                continue
            tentative_g = current_node.g + int(current_node.edges[neighbor.index])
            if neighbor not in open_list.keys():
                tentative_better = True
            elif tentative_g < neighbor.g:
                tentative_better = True
            else:
                tentative_better = False
            if tentative_better:
                came_from[neighbor.index] = current_node.index
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor.index, goal_index, nodes)
                neighbor.f = neighbor.g + neighbor.h
                open_list[neighbor] = 1


# calculate the h(n) with Manhattan Distance
def heuristic(current_index, goal_index, nodes):
    current_square = int(nodes[current_index].square)
    goal_square = int(nodes[goal_index].square)
    current_x = current_square % 10
    current_y = current_square // 10
    goal_x = goal_square % 10
    goal_y = goal_square // 10
    distance = abs(current_x - goal_x) + abs(current_y - goal_y)
    return distance
    # return 0


# return the node with the lowest f in the open list
def get_lowest_f(open_list):
    lowest_f = math.inf
    return_node = None
    for node in open_list.keys():
        if node.f < lowest_f:
            lowest_f = node.f
            return_node = node
    return return_node


# find the adjacent nodes for the current node
def get_neighbors(current_node, nodes):
    current_index = current_node.index
    children_list = list(nodes[current_index].edges.keys())
    children = []
    for child_index in children_list:
        child = nodes[child_index]
        children.append(child)
    return children
