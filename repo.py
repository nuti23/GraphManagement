
def is_correct_no_edges_vertices(no_vertices, no_edges):
    return no_edges == no_vertices(no_vertices - 1)


class Repository:

    def __init__(self, graph):
        self.graph = graph

    def add_vertex(self, vertex):
        self.graph.get_edges_in()[vertex] = []
        self.graph.get_edges_out()[vertex] = []
        self.graph.no_vertices += 1

    def remove_vertex(self, vertex):
        for predecessor in self.graph.get_edges_in()[vertex]:
            del self.graph.get_costs()[(predecessor, vertex)]
            self.graph.get_edges_out()[predecessor].remove(vertex)
            self.graph.no_edges -= 1

        for successor in self.graph.get_edges_out()[vertex]:
            del self.graph.get_costs()[(vertex, successor)]
            self.graph.get_edges_in()[successor].remove(vertex)
            self.graph.no_edges -= 1

        del self.graph.get_edges_in()[vertex]
        del self.graph.get_edges_out()[vertex]
        self.graph.no_vertices -= 1

    def add_edge(self, edge, cost):
        self.graph.get_costs()[edge] = cost
        self.graph.get_edges_out()[edge[0]].append(edge[1])
        self.graph.get_edges_in()[edge[1]].append(edge[0])
        self.graph.no_edges += 1

    def remove_edge(self, edge):
        del self.graph.get_costs()[edge]
        self.graph.get_edges_out()[edge[0]].remove(edge[1])
        self.graph.get_edges_in()[edge[1]].remove(edge[0])
        self.graph.no_edges -= 1

    def modify_cost(self, edge, new_cost):
        self.graph.get_costs()[edge] = new_cost

    def is_vertex(self, vertex):
        for vx in self.graph.vertices():
            if vx == vertex:
                return True
        return False

    def is_edge(self, edge):
        for eg in self.graph.edges():
            if eg == edge:
                return True
        return False

    def is_an_edge_between(self, vertex1, vertex2):
        edge = (vertex1, vertex2)
        return self.is_edge(edge)

    def get_in_degree_list(self, vertex):
        in_degree = []
        for vx in self.graph.get_edges_in()[vertex]:
            in_degree.append(vx)
        return in_degree

    def get_out_degree_list(self, vertex):
        out_degree = []
        for vx in self.graph.get_edges_out()[vertex]:
            out_degree.append(vx)
        return out_degree

    def get_vertices_repo(self):
        return self.graph.vertices()

    def get_edges_repo(self):
        return self.graph.edges()

    def get_cost_repo(self, edge):
        return self.graph.get_cost(edge)

