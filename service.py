import sys


class ServiceException(Exception):
    """
    Here we create Service exceptions that may occur.
    """
    def __init__(self, message=''):
        self._message = message


class Service:
    def __init__(self, repo):
        self.repo = repo

    def add_vertex_service(self, vertex):
        if isinstance(vertex, int):
            if not self.repo.is_vertex(vertex):
                self.repo.add_vertex(vertex)
            else:
                raise ServiceException("ATTENTION: this vertex already exists!")
        else:
            raise ServiceException("ATTENTION: vertex must be an int!")

    def remove_vertex_service(self, vertex):
        if isinstance(vertex, int):
            if self.repo.is_vertex(vertex):
                self.repo.remove_vertex(vertex)
            else:
                raise ServiceException("ATTENTION: this vertex does not exist!")
        else:
            raise ServiceException("ATTENTION: vertex must be an int!")

    def add_edge_service(self, start, stop, cost):
        if isinstance(start, int) and isinstance(stop, int) and isinstance(cost, int):
            if self.repo.is_vertex(start) and self.repo.is_vertex(stop):
                if not self.repo.is_edge((start, stop)):
                    self.repo.add_edge((start, stop), cost)
                else:
                    raise ServiceException("ATTENTION: this edge already exists!")
            else:
                raise ServiceException("ATTENTION: invalid vertices!")
        else:
            raise ServiceException("ATTENTION: vertices and cost must be ints!")

    def remove_edge_service(self, start, stop):
        if isinstance(start, int) and isinstance(stop, int):
            if self.repo.is_vertex(start) and self.repo.is_vertex(stop):
                if self.repo.is_edge((start, stop)):
                    self.repo.remove_edge((start, stop))
                else:
                    raise ServiceException("ATTENTION: this edge does not exist!")
            else:
                raise ServiceException("ATTENTION: invalid vertices!")
        else:
            raise ServiceException("ATTENTION: vertices must be ints!")

    def modify_cost_service(self, start, stop, new_cost):
        if isinstance(start, int) and isinstance(stop, int) and isinstance(new_cost, int):
            if self.repo.is_vertex(start) and self.repo.is_vertex(stop):
                if self.repo.is_edge((start, stop)):
                    self.repo.modify_cost((start, stop), new_cost)
                else:
                    raise ServiceException("ATTENTION: this edge does not exist!")
            else:
                raise ServiceException("ATTENTION: invalid vertices!")
        else:
            raise ServiceException("ATTENTION: vertices and new_cost must be ints!")

    def get_in_degree_list_service(self, vertex):
        if isinstance(vertex, int):
            if self.repo.is_vertex(vertex):
                in_degree = self.repo.get_in_degree_list(vertex)
            else:
                raise ServiceException("ATTENTION: this vertex does not exist!")
        else:
            raise ServiceException("ATTENTION: vertex must be an int!")
        return in_degree

    def get_out_degree_list_service(self, vertex):
        if isinstance(vertex, int):
            if self.repo.is_vertex(vertex):
                out_degree = self.repo.get_out_degree_list(vertex)
            else:
                raise ServiceException("ATTENTION: this vertex does not exist!")
        else:
            raise ServiceException("ATTENTION: vertex must be an int!")
        return out_degree

    def get_vertices_service(self):
        return self.repo.get_vertices_repo()

    def get_edges_service(self):
        return self.repo.get_edges_repo()

    def is_edge_between(self, start, stop):
        is_it = False
        if isinstance(start, int) and isinstance(stop, int):
            if self.repo.is_vertex(start) and self.repo.is_vertex(stop):
                if self.repo.is_edge((start, stop)):
                   is_it = self.repo.is_an_edge_between(start, stop)
                else:
                    raise ServiceException("ATTENTION: this edge does not exist!")
            else:
                raise ServiceException("ATTENTION: invalid vertices!")
        else:
            raise ServiceException("ATTENTION: vertices must be ints!")
        return is_it

    def get_cost_service(self, start, stop):
        is_it = self.is_edge_between(start, stop)
        if isinstance(start, int) and isinstance(stop, int):
            if self.repo.is_vertex(start) and self.repo.is_vertex(stop):
                if self.repo.is_edge((start, stop)):
                    if is_it:
                        return self.repo.get_cost_repo((start, stop))
                else:
                    raise ServiceException("ATTENTION: this edge does not exist!")
            else:
                raise ServiceException("ATTENTION: invalid vertices!")
        else:
            raise ServiceException("ATTENTION: vertices must be ints!")

    def get_isolated_vertices(self):
        isolated_vertices = []
        vertices = self.repo.get_vertices_repo()
        for v in vertices:
            if len(self.repo.get_in_degree_list(v)) == 0 and len(self.repo.get_out_degree_list(v)) == 0:
                isolated_vertices.append(v)
        return isolated_vertices

    def path(self, s):
        dist = [0] * (self.repo.graph.no_vertices + 1)
        prev = [0] * (self.repo.graph.no_vertices + 1)
        isolated = len(self.get_out_degree_list_service(s)) != 0 and len(self.get_in_degree_list_service(s)) != 0
        is_path=True
        visited = set()
        if(not isolated):
            visited.add(s)
            dist[s] = 0
            queue = [s]
            while len(queue) > 0:
                x = queue[0]
                queue = queue[1:]
                for y in self.get_out_degree_list_service(x):
                    if y not in visited:
                        visited.add(y)
                        queue.append(y)
                        dist[y] = dist[x]+1
                        prev[y] = x
        else:
            is_path = False
        return is_path, visited, dist, prev

    def lowest_path(self, s, t):
        is_path, visited, dist, prev = self.path(s)
        if (is_path and dist[t] !=0 ):
            lowest_path = []
            lowest_path.append(t)
            node = prev[t]
            lowest_path.append(node)
            while(node != s):
                node = prev[node]
                lowest_path.append(node)

            reversed_lowest_path = []

            for index in range(len(lowest_path)-1, -1, -1 ):
                reversed_lowest_path.append(lowest_path[index])

            return reversed_lowest_path
        else:
            raise ValueError

    def isNegCycleBellmanFord(self, start):
        V = self.repo.graph.no_vertices
        E = self.repo.graph.no_edges
        dist = [1000000 for i in range(V+1)]
        dist[start] = 0

        # Relax all edges |V| - 1 times.
        # A simple shortest path from src to any
        # other vertex can have at-most |V| - 1
        # edges
        for i in range(1, V):
            for a in self.repo.graph.edges():
                u = a[0]
                v = a[1]
                weight = self.repo.graph.get_cost((u, v))
                if (dist[u] != 1000000 and dist[u] + weight < dist[v]):
                    dist[v] = dist[u] + weight

        # check for negative-weight cycles.
        # The above step guarantees shortest distances
        # if graph doesn't contain negative weight cycle.
        # If we get a shorter path, then there
        # is a cycle.
        for d in dist:
            print(d)

        for a in self.repo.graph.edges():
            u = a[0]
            v = a[1]
            weight = self.repo.graph.get_cost((u, v))
            if (dist[u] != 1000000 and dist[u] + weight < dist[v]):
                return True

        return False

    def BelmanFord(self, start, stop):

        if not self.repo.is_vertex(start) or not self.repo.is_vertex(stop):
            raise ServiceException("NO PATH")

        # if len(self.repo.get_in_degree_list(start)) == 0 or len(self.repo.get_out_degree_list(start) == 0) or len(self.repo.get_in_degree_list(stop)) == 0 or len(self.repo.get_out_degree_list(stop) ==0):
        #     raise ServiceException("NO PATH")

        # infinity for vertices we cannot reach
        inf = float('inf')
        # -1 for prev in the beginning
        none = -1
        distance = []
        prev = []

        # initialize dist and prev
        for i in range(0,self.repo.graph.no_vertices):
            distance.append(inf)
            prev.append(none)
        distance[start] = 0
        prev[start] = none

        for index in range(0, self.repo.graph.no_vertices):
            # to run faster
            changed = False
            for e in self.repo.graph.edges():
                # start = e[0] to  stop = e[1] with cost = self.repo.graph.get_cost((start, stop))
                START = e[0]
                STOP = e[1]
                COST = self.repo.graph.get_cost((START, STOP))
                if distance[START] + COST < distance[STOP]:
                    distance[STOP] = distance[START] + COST
                    prev[STOP] = START
                    changed = True
            if not changed:
                break

        # we do another loop to see if we have negative cycles
        for e in self.repo.graph.edges():
            START = e[0]
            STOP = e[1]
            COST = self.repo.graph.get_cost((START, STOP))
            if distance[START] + COST < distance[STOP]:
                raise ServiceException("ATTENTION! NEGATIVE CYCLE DETECTED!")
        if distance[stop] == inf:
            raise ServiceException("NO PATH!")


        print("Distance: ", distance[stop])
        current = stop
        path = []
        while current!= start:
            path.append(current)
            current = prev[current]
        path.append(start)
        path.reverse()
        print(path)

    def bellman_ford2(self, src, stop):

            if not self.repo.is_vertex(src) or not self.repo.is_vertex(stop):
                raise ServiceException("NO PATH")

            # fill the distance array and predecessor array
            dist = [float("Inf")] * self.repo.graph.no_vertices
            # Mark the source vertex
            dist[src] = 0
            prev = [-1] * self.repo.graph.no_vertices
            prev[src] = -1

            # relax edges |V| - 1 times
            for _ in range(self.repo.graph.no_vertices - 1):
                hasRelaxed = False
                for e in self.repo.graph.edges():
                    # start = e[0] to  stop = e[1] with cost = self.repo.graph.get_cost((start, stop))
                    s = e[0]
                    d = e[1]
                    w = self.repo.graph.get_cost((s, d))
                    if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                        hasRelaxed = True
                        dist[d] = dist[s] + w
                        prev[d] = s
                if not hasRelaxed:
                    break

            # detect negative cycle
            # if value changes then we have a negative cycle in the graph
            # and we cannot find the shortest distances
            for e in self.repo.graph.edges():
                # start = e[0] to  stop = e[1] with cost = self.repo.graph.get_cost((start, stop))
                s = e[0]
                d = e[1]
                w = self.repo.graph.get_cost((s, d))
                if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                    raise ServiceException("ATTENTION! NEGATIVE CYCLE DETECTED!")

            if dist[stop] == float("Inf"):
                raise ServiceException("NO PATH!")

            print("Vertex Distance from Source To Destination")

            print("{0}\t\t{1}".format(src, dist[stop]))

            current = stop
            path = []
            while current != src:
                path.append(current)
                current = prev[current]
            path.append(src)
            path.reverse()
            print(path)


