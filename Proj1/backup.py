# useless file for abandoned codes backup


# # def dijkstra(start_point, vertices):
# #     unvisited_vertices = list(vertices.keys())  # list of which vertices need to be checked
# #     min_distances = {}  # dictionary {toIndex : minimum_distance}
# #     # min_path = {} # dictionary {toIndex : minimum_distance_path}
# #     # current_path = []  # use for traceback
# #     for unvisited_vertex in unvisited_vertices:
# #         if unvisited_vertex == start_point:
# #             min_distances[unvisited_vertex] = 0
# #         else:
# #             min_distances[unvisited_vertex] = math.inf
# #     visited_vertices = []
# #     current_vertex = start_point
# #     visited_vertices.append(current_vertex)
# #     #current_path.append(current_vertex)
# #     # print(current_vertex)
# #     # print(unvisited_vertices)
# #     unvisited_vertices.remove(current_vertex)
# #     # check_neighbor_distance(current_vertex, vertices, min_distances)
# #     while unvisited_vertices != []:
# #         check_neighbor_distance(current_vertex, vertices, min_distances)
# #         shortest_pair = get_shortest_element(current_vertex, visited_vertices, vertices)
# #         next_vertex = shortest_pair[1]
# #         # traceback if there is no valid further move from current vertex
# #         if next_vertex == '-1':
# #             current_vertex = get_valid_parent(current_vertex, current_path, unvisited_vertices, vertices)
# #             continue
# #         possible_shortest_distance = shortest_pair[0] + min_distances[current_vertex]
# #         if possible_shortest_distance < min_distances[next_vertex]:
# #             min_distances[next_vertex] = possible_shortest_distance
# #         unvisited_vertices.remove(next_vertex)
# #         visited_vertices.append(next_vertex)
# #         #current_path.append(next_vertex)
# #         current_vertex = next_vertex
# #         # check_neighbor_distance(current_vertex, vertices, min_distances)
# #     return min_distances
# #
# #
# # # traceback the next valid parent when there is no further step from current vertex
# # def get_valid_parent(current_vertex, current_path, unvisited_vertices, vertices):
# #     current_index = current_path.index(current_vertex)
# #     current_path.remove(current_vertex)
# #     parent = current_path[current_index - 1]
# #     parent_neighbors = list(vertices[parent].edges.keys())
# #     parent_validity = False
# #     for neighbor in parent_neighbors:
# #         if neighbor in unvisited_vertices:
# #             parent_validity = True
# #     if parent_validity:
# #         return parent
# #     else:
# #         return get_valid_parent(parent, current_path, unvisited_vertices, vertices)
# #
#
# # def dijkstra(start_point, vertices):
# #     unvisited_vertices = list(vertices.keys())  # list of which vertices need to be checked
# #     min_distances = {}  # dictionary {toIndex : minimum_distance}
# #     for unvisited_vertex in unvisited_vertices:
# #         if unvisited_vertex == start_point:
# #             min_distances[unvisited_vertex] = 0
# #         else:
# #             min_distances[unvisited_vertex] = math.inf
# #     current_vertex = start_point
# #     open_list = []
# #     open_list.append(current_vertex)
# #     unvisited_vertices.remove(current_vertex)
# #     check_neighbor_distance(current_vertex, vertices, min_distances)
# #     while unvisited_vertices!= []:
# #         print(min_distances['321'])
# #         shortest_pair = get_shortest_element(open_list, vertices, unvisited_vertices)
# #         next_vertex = shortest_pair[0]
# #         possible_shortest_distance = shortest_pair[1] + min_distances[current_vertex]
# #         # print(possible_shortest_distance)
# #         if possible_shortest_distance < min_distances[next_vertex]:
# #             min_distances[next_vertex] = possible_shortest_distance
# #         open_list.append(next_vertex)
# #         update_open_list(open_list, vertices, unvisited_vertices)
# #         current_vertex = next_vertex
# #         unvisited_vertices.remove(current_vertex)
# #         check_neighbor_distance(current_vertex, vertices, min_distances)
# #         # print(open_list)
# #     return min_distances
#
# # from vertex import Vertex
# # from copy import copy
# #
# #
# # def a_star(start_index, goal_index, nodes):
# #     open_list = []
# #     close_list = []
# #     start_node = copy(nodes[start_index])
# #     start_node.g = 0
# #     start_node.f = 0
# #     start_node.parent = Vertex('-1', '-1')
# #     open_list.append(start_node)
# #     # current_node = start_node
# #     while open_list != []:
# #         current_node = get_lowest_f(open_list)
# #         open_list.remove(current_node)
# #         children = get_children(current_node, nodes)
# #         for child in children:
# #             child.g = current_node.g + int(current_node.edges[child.index])
# #             child.h = heuristic(child.index, goal_index, nodes)
# #             child.f = child.g + child.h
# #             if check_exist(child, open_list):
# #                 continue
# #             if check_exist(child, close_list):
# #                 continue
# #             else:
# #                 open_list.append(child)
# #         close_list.append(current_node)
# #         if current_node.index == goal_index:
# #             break
# #     print(current_node)
# #
# #
# #
# # # use Manhattan Distance to get h
# # def heuristic(current_node, goal_node, nodes):
# #     current_square = int(nodes[current_node].square)
# #     goal_square = int(nodes[goal_node].square)
# #     current_x = current_square % 10
# #     current_y = current_square // 10
# #     goal_x = goal_square % 10
# #     goal_y = goal_square // 10
# #     distance = ((current_x - goal_x)) ** 2 + ((current_y - goal_y)) ** 2
# #     return distance ** 0.5
# #
# #
# # # generate the list of children Vertex objects
# # def get_children(current_node, nodes):
# #     current_index = current_node.index
# #     children_list = list(nodes[current_index].edges.keys())
# #     children = []
# #     for child_index in children_list:
# #         child = copy(nodes[child_index])
# #         if child.index == current_node.parent.index:
# #             continue
# #         child.parent = current_node
# #         children.append(child)
# #     return children
# #
# #
# # # find the node with the lowest f value in the open list
# # def get_lowest_f(open_list):
# #     lowest_f = open_list[0].f
# #     return_node = open_list[0]
# #     for node in open_list:
# #         if node.f < lowest_f:
# #             lowest_f = node.f
# #             return_node = node
# #     return return_node
# #
# #
# # # check whether there is a node with the same index but lower f existed in the list
# # def check_exist(node, waiting_list):
# #     exist = False
# #     for list_node in waiting_list:
# #         if (list_node.index == node.index) & (list_node.f < node.f):
# #             exist = True
# #     return exist
# #
# #
# # def calc_distance(goal):
# #     distance = 0
# #     current = goal
# #     path = []
# #     path.append(current.index)
# #     previous = current.parent
# #     while previous.index != '-1':
# #         distance += int(previous.edges[current.index])
# #         path.append(previous.index)
# #         current = previous
# #         previous = current.parent
# #     return path, distance
# #
#
#
#
#
# from copy import copy
# from vertex import Vertex
#
#
# def a_star(start_index, goal_index, nodes):
#     close_list = []
#     open_list = []
#     came_from = {}
#     start_node = nodes[start_index]
#     start_node.g = 0
#     start_node.h = heuristic(start_node.index, goal_index, nodes)
#     start_node.f = start_node.g + start_node.h
#     # start_node.parent = Vertex('-1', '-1')
#     open_list.append(start_node)
#     while open_list != []:
#         current_node = get_lowest_f(open_list)
#         print(current_node.index)
#         if current_node.index == goal_index:
#             break
#         open_list.remove(current_node)
#         close_list.append(current_node)
#         for neighbor in get_neighbors(current_node,nodes):
#             if neighbor in close_list:
#                 continue
#             tentative_g = current_node.g + int(current_node.edges[neighbor.index])
#             if neighbor not in open_list:
#                 tentative_better = True
#             elif tentative_g < neighbor.g:
#                 tentative_better = True
#             else:
#                 tentative_better = False
#             if tentative_better:
#                 came_from[neighbor.index] = current_node.index
#                 neighbor.g = tentative_g
#                 neighbor.h = heuristic(neighbor.index, goal_index, nodes)
#                 neighbor.f = neighbor.g + neighbor.h
#                 open_list.append(neighbor)
#     return current_node.index
#
#
# def heuristic(current_index, goal_index, nodes):
#     current_square = int(nodes[current_index].square)
#     goal_square = int(nodes[goal_index].square)
#     current_x = current_square % 10
#     current_y = current_square // 10
#     goal_x = goal_square % 10
#     goal_y = goal_square // 10
#     distance = ((current_x - goal_x) * 10) ** 2 + ((current_y - goal_y) * 10) ** 2
#     return distance
#
#
# # def get_path(came_from, current_node):
# #     print("start path release")
# #     path = []
# #     current_index = current_node.index
# #     print(came_from)
# #     while len(came_from) > 0:
# #         previous_index = came_from[current_index]
# #         path.append(current_index)
# #         del came_from[current_index]
# #         current_index = previous_index
# #     return path
#
#
# def get_lowest_f(open_list):
#     lowest_f = open_list[0].f
#     return_node = open_list[0]
#     for node in open_list:
#         if node.f < lowest_f:
#             lowest_f = node.f
#             return_node = node
#     return return_node
#
#
# def get_neighbors(current_node, nodes):
#     current_index = current_node.index
#     children_list = list(nodes[current_index].edges.keys())
#     children = []
#     for child_index in children_list:
#         child = nodes[child_index]
#         children.append(child)
#     return children
#
#
#
# from copy import copy
# from vertex import Vertex
#
#
# def a_star(start_index, goal_index, nodes):
#     close_list = []
#     open_list = []
#     came_from = {}
#     start_node = nodes[start_index]
#     start_node.g = 0
#     start_node.h = heuristic(start_node.index, goal_index, nodes)
#     start_node.f = start_node.g + start_node.h
#     # start_node.parent = Vertex('-1', '-1')
#     open_list.append(start_node)
#     while open_list != []:
#         current_node = get_lowest_f(open_list)
#         print(current_node.index)
#         if current_node.index == goal_index:
#             break
#         open_list.remove(current_node)
#         close_list.append(current_node)
#         for neighbor in get_neighbors(current_node,nodes):
#             if neighbor in close_list:
#                 continue
#             tentative_g = current_node.g + int(current_node.edges[neighbor.index])
#             if neighbor not in open_list:
#                 tentative_better = True
#             elif tentative_g < neighbor.g:
#                 tentative_better = True
#             else:
#                 tentative_better = False
#             if tentative_better:
#                 came_from[neighbor.index] = current_node.index
#                 neighbor.g = tentative_g
#                 neighbor.h = heuristic(neighbor.index, goal_index, nodes)
#                 neighbor.f = neighbor.g + neighbor.h
#                 open_list.append(neighbor)
#     return current_node.index
#
#
# def heuristic(current_index, goal_index, nodes):
#     current_square = int(nodes[current_index].square)
#     goal_square = int(nodes[goal_index].square)
#     current_x = current_square % 10
#     current_y = current_square // 10
#     goal_x = goal_square % 10
#     goal_y = goal_square // 10
#     distance = ((current_x - goal_x) * 10) ** 2 + ((current_y - goal_y) * 10) ** 2
#     return distance
#
#
# # def get_path(came_from, current_node):
# #     print("start path release")
# #     path = []
# #     current_index = current_node.index
# #     print(came_from)
# #     while len(came_from) > 0:
# #         previous_index = came_from[current_index]
# #         path.append(current_index)
# #         del came_from[current_index]
# #         current_index = previous_index
# #     return path
#
#
# def get_lowest_f(open_list):
#     lowest_f = open_list[0].f
#     return_node = open_list[0]
#     for node in open_list:
#         if node.f < lowest_f:
#             lowest_f = node.f
#             return_node = node
#     return return_node
#
#
# def get_neighbors(current_node, nodes):
#     current_index = current_node.index
#     children_list = list(nodes[current_index].edges.keys())
#     children = []
#     for child_index in children_list:
#         child = nodes[child_index]
#         children.append(child)
#     return children
#
#
