from vertex import Vertex


# add edges to the Vertex object dict
def update_vertex(vertex_old, to_index, cost):
    vertex = vertex_old
    vertex.add_edge(to_index,cost)
    return vertex


def generate_map(vertex_file, edge_file):
    f1 = open(vertex_file, 'r')
    # generate Vertex object dict {vertex_index(str) : Vertex(object)}
    vertices_info = f1.readlines()
    vertices = {}
    for vertex_info in vertices_info:
        if vertex_info[0] == '#':
            continue
        vertex_info_split = vertex_info.strip().split(',')
        one_vertex = Vertex(vertex_info_split[0], vertex_info_split[1])
        vertices[one_vertex.index] = one_vertex
    f1.close()
    f2 = open(edge_file, 'r')
    edges_info = f2.readlines()
    # from fromIndex to toIndex
    for edge_info in edges_info:
        if edge_info[0] == '#':
            continue
        edge_info_split = edge_info.strip().split(',')
        vertices[edge_info_split[0]] = update_vertex(vertices[edge_info_split[0]], edge_info_split[1], edge_info_split[2])
    # from toIndex to fromIndex
    for edge_info in edges_info:
        if edge_info[0] == '#':
            continue
        edge_info_split = edge_info.strip().split(',')
        vertices[edge_info_split[1]] = update_vertex(vertices[edge_info_split[1]], edge_info_split[0], edge_info_split[2])
    f2.close()
    return vertices

















