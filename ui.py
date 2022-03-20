import random

from domain import Graph
from repo import Repository
from service import ServiceException, Service


def menu():
    print("----VERTEX ZONE----")
    print("(1) ADD a vertex")
    print("(2) DELETE a vertex")
    print("(3) is EDGE between?")
    print("(4) PRINT all vertices")
    print("(5) NO. of vertices")
    print("(6) INBOUND of a vertex")
    print("(7) OUTBOUND of a vertex")
    print("-----EDGE ZONE-----")
    print("(8) ADD an edge")
    print("(9) DELETE an edge")
    print("(10) PRINT all edges")
    print("(11) NO. of edges")
    print("(12) COST of an edge")
    print("(13) MODIFY COST")
    print("------------------")
    print("(14) SAVE the graph")
    print("(15) GENERATE random graph")
    print("(16) READ from file")
    print("(17) READ from file2")
    print("(18) LOWEST PATH between 2 vertices")
    print("(19) BELLMAN FORD")

def print_list(list):
    for elem in list:
        print(elem)


class Ui:
    def __init__(self, service):
        self.service = service

    def add_vertex_ui(self):
        print("adding a vertex...")
        print()
        vertex = input("enter vertex: ")
        try:
            vertex = int(vertex)
        except ValueError as ve:
            print(ve)
        try:
            self.service.add_vertex_service(vertex)
        except ServiceException as se:
            print(se)

    def remove_vertex_ui(self):
        print("removing a vertex...")
        print()
        vertex = input("enter vertex: ")
        try:
            vertex = int(vertex)
        except ValueError as ve:
            print(ve)
        try:
            self.service.remove_vertex_service(vertex)
        except ServiceException as se:
            print(se)

    def in_degree_list_ui(self):
        print("IN DEGREE of a vertex...")
        print()
        vertex = input("enter vertex: ")
        try:
            vertex = int(vertex)
        except ValueError as ve:
            print(ve)
        try:
            list = self.service.get_in_degree_list_service(vertex)
            if(len(list) != 0):
                print("list: ")
                print_list(list)
            print("INdegree: ", len(list))
        except ServiceException as se:
            print(se)

    def out_degree_list_ui(self):
        print("OUT DEGREE of a vertex...")
        print()
        vertex = input("enter vertex: ")
        try:
            vertex = int(vertex)
        except ValueError as ve:
            print(ve)
        try:
            list = self.service.get_out_degree_list_service(vertex)
            if (len(list) != 0):
                print("list: ")
                print_list(list)
            print("OUTdegree: ", len(list))
        except ServiceException as se:
            print(se)

    def add_edge_ui(self):
        print("adding an edge...")
        print()
        start = input("enter start vertex: ")
        stop = input("enter stop vertex: ")
        cost = input("enter the cost: ")
        try:
            start = int(start)
            stop = int(stop)
            cost = int(cost)
        except ValueError as ve:
            print(ve)
        try:
            self.service.add_edge_service(start, stop, cost)
        except ServiceException as se:
            print(se)

    def remove_edge_ui(self):
        print("removing an edge...")
        print()
        start = input("enter start vertex: ")
        stop = input("enter stop vertex: ")
        try:
            start = int(start)
            stop = int(stop)
        except ValueError as ve:
            print(ve)
        try:
            self.service.remove_edge_service(start, stop)
        except ServiceException as se:
            print(se)

    def is_edge_ui(self):
        is_it = False
        print("is edge between?...")
        print()
        start = input("enter start vertex: ")
        stop = input("enter stop vertex: ")
        try:
            start = int(start)
            stop = int(stop)
        except ValueError as ve:
            print(ve)
        try:
            is_it = self.service.is_edge_between(start, stop)
        except ServiceException as se:
            print(se)
        print(is_it)

    def print_vertices(self):
        print_list(self.service.get_vertices_service())

    def print_no_vertices(self):
        print(len(self.service.get_vertices_service()))

    def print_no_edges(self):
        print(len(self.service.get_edges_service()))

    def print_edges(self):
        print_list(self.service.get_edges_service())

    def modify_cost_ui(self):
        print("modifying a cost...")
        print()
        start = input("enter start vertex: ")
        stop = input("enter stop vertex: ")
        cost = input("enter the new cost: ")
        try:
            start = int(start)
            stop = int(stop)
            cost = int(cost)
        except ValueError as ve:
            print(ve)
        try:
            self.service.modify_cost_service(start, stop, cost)
        except ServiceException as se:
            print(se)

    def print_cost_edge_ui(self):
        start = input("enter start vertex: ")
        stop = input("enter stop vertex: ")
        try:
            start = int(start)
            stop = int(stop)
        except ValueError as ve:
            print(ve)
        print("cost of given edge is:")
        try:
            print(self.service.get_cost_service(start, stop))
        except ServiceException as se:
            print(se)

    def read_from_file_ui(self):
        filename = input("enter filename.extension : ")
        self.read_from_file(filename)

    def read_from_file(self, filename):
        first = True
        with open(filename, 'r') as f:
            for line in f:
                line = line.split()
                if first:
                    first = False
                    vertices = int (line[0])
                    for v in range(vertices):
                        self.service.add_vertex_service(v)
                else:
                    self.service.add_edge_service(int(line[0]), int(line[1]), int(line[2]))

    def read_from_file_2_ui(self):
        filename = input("enter filename.extension: ")
        self.read_from_file_2(filename)

    def read_from_file_2(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.split()
                if len(line) == 1:
                    if not self.service.repo.is_vertex(int(line[0])):
                        self.service.add_vertex_service(int(line[0]))
                else:
                    if len(line) == 3:
                        if not self.service.repo.is_vertex(int(line[0])):
                            self.service.add_vertex_service(int(line[0]))
                        if not self.service.repo.is_vertex(int(line[1])):
                            self.service.add_vertex_service(int(line[1]))
                        self.service.add_edge_service(int(line[0]), int(line[1]), int(line[2]))

    def write_to_file(self, filename):
         with open(filename, "w") as f:
             f.write(str(self.service.repo.graph.no_vertices) + " " + str(self.service.repo.graph.no_edges) + "\n")
             for element in self.service.get_edges_service():
                 f.write(str(element[0]) + " " + str(element[1]) + " " + str(self.service.get_cost_service(element[0], element[1])) + "\n")
             for elem in self.service.get_isolated_vertices():
                 f.write(str(elem) + "\n")

    def write_to_file_ui(self):
        filename = input("enter filename.extension : ")
        self.write_to_file(filename)

    def create_random_graph_ui(self, filename):
        vertices = input("enter no vertices: ")
        edges = input("enter no edges: ")
        try:
            vertices = int(vertices)
            edges = int(edges)

        except ValueError as ve:
            print(ve)
        create_random_graph(vertices, edges, filename)

    def lowest_path_ui(self):
        start = input("enter start vertex: ")
        stop = input("enter stop vertex: ")
        try:
            start = int(start)
            stop = int(stop)
        except ValueError as ve:
            print(ve)

        try:
            lowest_path=self.service.lowest_path(start, stop)
            for vertex in lowest_path:
                print(vertex)
            print("LENGTH: ", len(lowest_path)-1)
        except ValueError as v:
            print("ERROR : no path")

    def bellman_ford(self):
        start = input("enter start vertex: ")
        stop = input("enter stop vertex: ")
        try:
            start = int(start)
            stop = int(stop)
        except ValueError as ve:
            print(ve)

        try:
            self.service.bellman_ford2(start, stop)
        except ServiceException as se:
            print(se)



    def start(self):
        print("Welcome!")
        while True:
            print()
            menu()
            print()
            OPTION = input('Enter your option: ')

            try:
                OPTION = int(OPTION)
            except ValueError as ve:
                print(ve)

            if OPTION == 0:
                print("See you next time!")
                break
            elif OPTION == 1:
                self.add_vertex_ui()
            elif OPTION == 2:
                self.remove_vertex_ui()
            elif OPTION == 3:
                self.is_edge_ui()
            elif OPTION == 4:
                self.print_vertices()
            elif OPTION == 5:
                self.print_no_vertices()
            elif OPTION == 6:
                self.in_degree_list_ui()
            elif OPTION == 7:
                self.out_degree_list_ui()
            elif OPTION == 8:
                self.add_edge_ui()
            elif OPTION == 9:
                self.remove_edge_ui()
            elif OPTION == 10:
                self.print_edges()
            elif OPTION == 11:
                self.print_no_edges()
            elif OPTION == 12:
                self.print_cost_edge_ui()
            elif OPTION == 13:
                self.modify_cost_ui()
            elif OPTION == 14:
                self.write_to_file_ui()
            elif OPTION == 15:
                self.create_random_graph_ui("random_graph1.txt")
            elif OPTION == 16:
                self.read_from_file_ui()
            elif OPTION == 17:
                self.read_from_file_2_ui()
            elif OPTION == 18:
                self.lowest_path_ui()
            elif OPTION == 19:
                self.bellman_ford()
            else:
                print("WRONG OPTION!")


def create_random_graph(vertices, edges, filename):
    if edges <= vertices*(vertices-1) and edges >-1 and vertices >-1:
        graph = Graph(vertices, 0)
        repo = Repository(graph)
        service = Service(repo)
        ui = Ui(service)
        e = edges -1
        while e >= 0:
            start = int(random.randint(0, vertices - 1))
            stop = int(random.randint(0, vertices - 1))
            cost = random.randint(0, 1000)
            if start != stop:
                if ui.service.repo.is_vertex(start) and ui.service.repo.is_vertex(stop):
                    if not ui.service.repo.is_edge((start, stop)):
                        ui.service.add_edge_service(start, stop, cost)
                        e -= 1

        ui.write_to_file(filename)
    else:
        f = open(filename, 'w')
        f.write("wrong number of edges or vertices")

