from domain import Graph
from repo import Repository
import unittest

from service import Service, ServiceException


class Test(unittest.TestCase):

    def test_domain_repo(self):
        graph = Graph(5, 10)
        repo = Repository(graph)
        self.assertTrue(graph.no_vertices == 5)
        repo.add_vertex(6)
        self.assertTrue(graph.no_vertices == 6)
        repo.remove_vertex(4)
        self.assertTrue(graph.no_vertices == 5)

        graph1 = Graph(0, 0)
        repo1 = Repository(graph1)
        repo1.add_vertex(1)
        repo1.add_vertex(2)
        repo1.add_vertex(3)
        repo1.add_vertex(4)
        self.assertTrue(graph1.no_vertices == 4)
        self.assertTrue(repo1.is_vertex(1))
        self.assertTrue(repo1.is_vertex(2))
        self.assertTrue(repo1.is_vertex(3))
        self.assertTrue(repo1.is_vertex(4))
        self.assertFalse(repo1.is_vertex(5))
        self.assertFalse(repo1.is_vertex(6))


        edge1 = (1, 4)
        cost1 = 30
        edge2 = (3, 4)
        cost2 = 60
        repo1.add_edge(edge1, cost1)
        self.assertTrue(repo1.is_edge(edge1))
        self.assertFalse(repo1.is_edge(edge2))
        repo1.add_edge(edge2, cost2)
        self.assertTrue(repo1.is_edge(edge2))
        repo1.modify_cost(edge2, 1000)
        self.assertTrue(repo1.graph.get_costs()[edge2] == 1000)
        self.assertTrue(repo1.is_an_edge_between(1, 4))
        self.assertFalse(repo1.is_an_edge_between(1, 2))

    def test_service(self):
        graph1 = Graph(0, 0)
        repo1 = Repository(graph1)
        service1 = Service(repo1)

        service1.add_vertex_service(1)
        self.assertRaises(ServiceException, service1.add_vertex_service, 1)

        service1.add_vertex_service(2)
        service1.add_vertex_service(3)
        service1.add_vertex_service(4)
        service1.add_vertex_service(5)
        self.assertTrue(service1.repo.graph.no_vertices == 5)

        service1.remove_vertex_service(1)
        self.assertRaises(ServiceException, service1.remove_vertex_service, 1)
        self.assertRaises(ServiceException, service1.remove_vertex_service, 100)
        self.assertTrue(service1.repo.graph.no_vertices == 4)

        service1.add_edge_service(2, 3, 100)
        self.assertRaises(ServiceException, service1.add_edge_service, 2, 3, 100)
        self.assertRaises(ServiceException, service1.add_edge_service, 20, 30, 100)

        service1.modify_cost_service(2, 3, 200)
        # TODO: GET_COST
        self.assertRaises(ServiceException, service1.modify_cost_service, 0, 0, 2)
        self.assertRaises(ServiceException, service1.modify_cost_service, 2, 4, 2)

        service1.remove_edge_service(2, 3)
        self.assertRaises(ServiceException, service1.remove_edge_service, 2, 3)
        self.assertRaises(ServiceException, service1.remove_edge_service, 20, 30)

        service1.add_edge_service(2, 3, 100)
        service1.add_edge_service(2, 4, 100)
        service1.add_edge_service(2, 5, 100)
        service1.add_edge_service(5, 2, 100)

        self.assertTrue(len(service1.get_in_degree_list_service(2)) == 1)
        self.assertTrue(len(service1.get_out_degree_list_service(2)) == 3)

        self.assertRaises(ServiceException, service1.get_out_degree_list_service, 24)
        self.assertRaises(ServiceException, service1.get_in_degree_list_service, 24)

        service1.remove_vertex_service(2)

    def test_copy(self):
        graph1 = Graph(0, 0)

        repo1 = Repository(graph1)
        service1 = Service(repo1)

        service1.add_vertex_service(1)
        service1.add_vertex_service(2)
        service1.add_vertex_service(3)
        self.assertTrue(graph1.no_vertices == 3)

        list = graph1.vertices()

        new_graph = graph1.COPY()
        new_list = new_graph.vertices()

        new_repo = Repository(new_graph)
        new_service = Service(new_repo)
        self.assertTrue(new_graph.no_vertices == 3)

        new_service.remove_vertex_service(1)
        self.assertTrue(new_graph.no_vertices == 2)
        self.assertTrue(graph1.no_vertices == 3)

    def test_path(self):
        graph1 = Graph(0, 0)
        repo1 = Repository(graph1)
        service1 = Service(repo1)


        service1.add_vertex_service(1)
        service1.add_vertex_service(2)
        service1.add_vertex_service(3)
        service1.add_vertex_service(4)
        service1.add_vertex_service(5)
        service1.add_vertex_service(6)

        service1.add_edge_service(1,2,0)
        service1.add_edge_service(2,3,0)
        service1.add_edge_service(2,4,0)
        service1.add_edge_service(3,4,0)
        service1.add_edge_service(4,6,0)
        service1.add_edge_service(5,3,0)
        service1.add_edge_service(5,6,0)

        is_path, visited, dist, prev = service1.path(1)

        for l in visited:
            print(l)
        print("----------")

        for l in dist:
            print(l)
        print("----------")

        for l in prev:
            print(l)
        print("----------")

        lowest_path = service1.lowest_path(1, 6)

        for l in lowest_path:
            print(l)

    def test_bellman(self):
        graph1 = Graph(0, 0)
        repo1 = Repository(graph1)
        service1 = Service(repo1)

        service1.add_vertex_service(0)
        service1.add_vertex_service(1)
        service1.add_vertex_service(2)
        service1.add_vertex_service(3)
        service1.add_vertex_service(4)
        service1.add_vertex_service(5)

        service1.add_edge_service(0, 1, -1)
        service1.add_edge_service(0, 2, 4)
        service1.add_edge_service(1, 2, 3)
        service1.add_edge_service(1, 3, 2)
        service1.add_edge_service(1, 4, 2)
        service1.add_edge_service(3, 2, 5)
        service1.add_edge_service(3, 1, -20)
        service1.add_edge_service(4, 3, -3)

        print(service1.isNegCycleBellmanFord(0))

    def test_bellman_ford(self):
        graph1 = Graph(0, 0)
        repo1 = Repository(graph1)
        service1 = Service(repo1)

        service1.add_vertex_service(0)
        service1.add_vertex_service(1)
        service1.add_vertex_service(2)
        service1.add_vertex_service(3)
        service1.add_vertex_service(4)
        service1.add_vertex_service(5)

        service1.add_edge_service(0, 1, -1)
        service1.add_edge_service(0, 2, 4)
        service1.add_edge_service(1, 2, 3)
        service1.add_edge_service(1, 3, 2)
        service1.add_edge_service(1, 4, 2)
        service1.add_edge_service(3, 2, 5)
        service1.add_edge_service(3, 1, -20)
        service1.add_edge_service(4, 3, -3)

        service1.BelmanFord(0,5)

    def test_all(self):
        pass
        #self.test_domain_repo()
        #self.test_service()
        #self.test_copy()
        #self.test_path()
        #self.test_bellman()


