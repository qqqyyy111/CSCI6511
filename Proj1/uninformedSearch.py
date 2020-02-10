import math


# main method for dijkstra(uninformed search), which will take the start point index(str), and the vertices map(dict)
def dijkstra(start_point, vertices):
    unvisited_vertices = {} # dict of which vertices need to be checked
    temp_list = list(vertices.keys())  # list for creating unvisited vertices dict
    for vertex in temp_list:
        unvisited_vertices[vertex] = 1
    visited_list = {}
    min_distances = {}  # dictionary {toIndex : minimum_distance}
    for unvisited_vertex in unvisited_vertices.keys():
        if unvisited_vertex == start_point:
            min_distances[unvisited_vertex] = 0
        else:
            min_distances[unvisited_vertex] = math.inf
    current_vertex = start_point
    open_list = {}  # contains all possible next moves {toIndex : distance}
    update_open_list(current_vertex,vertices, min_distances, open_list, visited_list)
    del unvisited_vertices[current_vertex]
    visited_list[current_vertex] = 1
    while len(unvisited_vertices) != 0:
        shortest_pair = get_shortest_element(open_list)
        current_vertex = shortest_pair[0]
        if min_distances[current_vertex] > shortest_pair[1]:
            min_distances[current_vertex] = shortest_pair[1]
        update_open_list(current_vertex, vertices, min_distances, open_list, visited_list)
        visited_list[current_vertex] = 1
        del unvisited_vertices[current_vertex]
    return min_distances


# check whether the distance from current vertex to the neighbor is the shortest distance
# if the nodes is unvisited, then add it to the open list, otherwise, check whether the node in the
# open list, which has the same index as the neighbor, if it does, ignore the node, not then update the open list
def update_open_list(current_vertex, vertices, min_distances, open_list, visited_list):
    neighbors = list(vertices[current_vertex].edges.keys())
    for neighbor in neighbors:
        distance = int(vertices[current_vertex].edges[neighbor])
        if neighbor in visited_list.keys():
            possible_minimum = int(vertices[current_vertex].edges[neighbor]) + min_distances[current_vertex]
            if possible_minimum < min_distances[neighbor]:
                min_distances[neighbor] = possible_minimum
        else:
            if neighbor in open_list.keys():
                if (distance + min_distances[current_vertex]) > open_list[neighbor]:
                    continue
            open_list[neighbor] = min_distances[current_vertex] + distance


# find the shortest path & distance from current vertex to the unvisited neighbors
def get_shortest_element(open_list):
    shortest = math.inf
    min_vertex = '-1'
    for path in open_list.items():
        if path[1] < shortest:
            shortest = path[1]
            min_vertex = path[0]
    del open_list[min_vertex]
    return min_vertex, shortest



