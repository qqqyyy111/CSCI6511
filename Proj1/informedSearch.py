import math
import heapq


# main method for A*(informed search), which will take the index of start point(str),the index of end point(str),
# and the nodes map(dict)
def a_star(start_index, goal_index, nodes):
    if start_index == goal_index:
        return 0, 0
    # close_list = {}  # list for nodes which have already evaluated, use for path track
    open_list = []
    goal_in_open_list = 0
    step_count = 0
    g_values = {}
    g_values[start_index] = 0
    f = g_values[start_index] + int(heuristic(start_index, goal_index, nodes))
    heapq.heappush(open_list, (f, start_index))
    # close_list[start_index] = None
    while open_list:
        current_pair = heapq.heappop(open_list)
        current_index = current_pair[1]
        step_count += 1
        # arrive the goal node, stop searching
        if current_index == goal_index:
            goal_in_open_list -= 1
            # if not check_node_existence(current_index, open_list):
            if goal_in_open_list < 1:
                return g_values[current_index], step_count
        for neighbor in nodes[current_index].edges.keys():
            tentative_g = g_values[current_index] + int(nodes[current_index].edges[neighbor])
            if (neighbor not in g_values.keys()) or (tentative_g < g_values[neighbor]):
                g_values[neighbor] = tentative_g
                f = int(heuristic(neighbor, goal_index, nodes)) + tentative_g
                heapq.heappush(open_list, (f, neighbor))
                if neighbor == goal_index:
                    goal_in_open_list += 1
                    # print(goal_in_open_list)
                # close_list[neighbor] = current_index


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


# check whether there is a pair contains goal node in the list
def check_node_existence(target_index, open_list):
    for pair in open_list:
        node_index = pair[1]
        if node_index == target_index:
            return True
    return False
