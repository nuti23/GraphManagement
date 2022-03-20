
import copy

class Graph:
    def __init__(self, no_vertices, no_edges):
        self._no_edges = no_edges
        self._no_vertices = no_vertices
        self._edges_in = {}
        self._edges_out = {}
        self._costs = {}

        for vertex in range(no_vertices):
            self._edges_in[vertex] = []
            self._edges_out[vertex] = []

    @property
    def no_edges(self):
        return self._no_edges

    @no_edges.setter
    def no_edges(self, value):
        self._no_edges = value

    @property
    def no_vertices(self):
        return self._no_vertices

    @no_vertices.setter
    def no_vertices(self, value):
        self._no_vertices = value

    def get_edges_in(self):
        return self._edges_in

    def get_edges_out(self):
        return self._edges_out

    def get_costs(self):
        return self._costs

    def vertices(self):
        return self._edges_in.keys()

    def edges(self):
        return self._costs.keys()

    def get_cost(self, edge):
        return self._costs[edge]

    def COPY(self):
        new_graph = Graph(0, 0)
        new_graph._no_vertices = self.no_vertices
        new_graph._no_edges = self.no_edges
        new_graph._edges_in = copy.deepcopy(self._edges_in)
        new_graph._edges_out = copy.deepcopy(self._edges_out)
        new_graph._costs = copy.deepcopy(self._costs)

        return new_graph
5




