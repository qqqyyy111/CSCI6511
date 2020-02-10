class Vertex:
    def __init__(self, index, square):
        self.index = index
        self.square = square
        self.edges = {}

    def add_edge(self, to_index, edge_cost):
        self.edges[to_index] = edge_cost


