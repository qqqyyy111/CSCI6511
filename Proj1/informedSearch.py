import math


# main method for A*(informed search), which will take the index of start point(str),the index of end point(str),
# and the nodes map(dict)
def a_star(start_index, goal_index, nodes):
    close_list = {}  # list for nodes which have already evaluated
    open_list = {}  # list for noes which need to be evaluated
    h_values = {}
    g_values = {}
    f_values = {}
    start_node = nodes[start_index]
    g_values[start_node.index] = 0
    h_values[start_node.index] = int(heuristic(start_node.index, goal_index, nodes))
    f_values[start_node.index] = g_values[start_node.index] + h_values[start_node.index]
    open_list[start_node] = 1
    close_list[start_node.index] = None
    while open_list:
        current_node = get_lowest_f(open_list, f_values)
        del open_list[current_node]
        # arrive the goal node, stop searching
        if current_node.index == goal_index:
            return g_values[current_node.index], close_list
        neighbors = get_neighbors(current_node, nodes)
        for neighbor in neighbors:
            tentative_g = g_values[current_node.index] + int(current_node.edges[neighbor.index])
            if (neighbor.index not in g_values.keys()) or (tentative_g < g_values[neighbor.index]):
                g_values[neighbor.index] = tentative_g
                h_values[neighbor.index] = int(heuristic(neighbor.index, goal_index, nodes))
                f_values[neighbor.index] = g_values[neighbor.index] + h_values[neighbor.index]
                open_list[neighbor] = 1
                close_list[neighbor.index] = current_node.index


# calculate the h(n) with Euclidean Distance
def heuristic(current_index, goal_index, nodes):
    current_square = int(nodes[current_index].square)
    goal_square = int(nodes[goal_index].square)
    current_x = current_square % 10
    current_y = current_square // 10
    goal_x = goal_square % 10
    goal_y = goal_square // 10
    x_difference = max(abs(current_x - goal_x) - 1, 0) * 10
    y_difference = max(abs(current_y - goal_y) - 1, 0) * 10
    distance = math.sqrt(math.pow(x_difference, 2) + math.pow(y_difference, 2))
    return distance
    # return 0


# return the node with the lowest f in the open list
def get_lowest_f(open_list, f_values):
    lowest_f = math.inf
    return_node = None
    for node in open_list.keys():
        if f_values[node.index] < lowest_f:
            lowest_f = f_values[node.index]
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


