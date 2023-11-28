from typing import Callable
from csv import DictReader
from functools import reduce


Vertex = int | float | str | tuple
Weight = int | float


class Graph(dict[Vertex, dict[Vertex, Weight]]):
    @staticmethod
    def from_csv(filename, source_column, destination_column, weight_column=None):
        g = Graph()

        with open(filename, "r") as file:
            reader = DictReader(file)

            for row in reader:
                source = row[source_column]
                destination = row[destination_column]
                weight = row[weight_column] if weight_column else None

                if not g.has_vertex(source):
                    g.add_vertex(source)

                if not g.has_vertex(destination):
                    g.add_vertex(destination)

                if not g.has_edge(source, destination):
                    if weight:
                        g.add_edge(source, destination, float(weight))

                    else:
                        g.add_edge(source, destination)

        return g

    def bfs_tree(self, s: Vertex):
        state = {k: -1 for k in self.vertices()}
        distance = {k: -1 for k in self.vertices()}
        parent = {k: None for k in self.vertices()}

        queue = []
        enqueue = queue.append
        dequeue = lambda: queue.pop(0)

        state[s] = 0
        distance[s] = 0
        parent[s] = None

        enqueue(s)
        while len(queue) > 0:
            u = dequeue()
            for v in self[u]:
                if state[v] == -1:
                    state[v] = 0
                    distance[v] = distance[u] + 1
                    parent[v] = u
                    enqueue(v)
            state[u] = 1

        tree = [(p, c) for c, p in parent.items() if p is not None]

        return tree

    def dfs_tree_recursive(self, s: Vertex):
        marked = {k: False for k in self.vertices()}
        tree = []

        def dfs(u: Vertex):
            marked[u] = True
            for v in self[u]:
                if not marked[v]:
                    tree.append((u, v))
                    dfs(v)

        dfs(s)

        return tree

    def dfs_tree(self, s: Vertex):
        parent = {k: None for k in self.vertices()}
        marked = {k: False for k in self.vertices()}

        stack = []
        push = stack.append
        pop = stack.pop

        push(s)

        while len(stack) > 0:
            u = pop()

            if not marked[u]:
                marked[u] = True

                for v in self[u]:
                    if not marked[v]:
                        parent[v] = u
                    push(v)

        tree = [(p, c) for c, p in parent.items() if p is not None]

        return tree

    def dijkstra(self, u: Vertex):
        distance = {k: float("inf") for k in self.vertices()}
        previous = {k: None for k in self.vertices()}
        explored = {k: False for k in self.vertices()}

        distance[u] = 0

        while False in explored.values():
            # Get vertex v as the lightest-weighted unexplored vertex
            v = reduce(
                lambda acc, x: acc if distance[acc] < distance[x] else x,
                [k for k in explored.keys() if not explored[k]],
            )

            # Set vertex v to explored
            explored[v] = True

            #
            for w in self.adjacency(v):
                if (distance[v] + self.get_edge_weight(v, w)) < distance[w]:
                    distance[w] = distance[v] + self.get_edge_weight(v, w)
                    previous[w] = v

        def get_path(v: Vertex | None):
            return str(u) if v is u else f"{v} <- {get_path(previous[v])}"

        paths = [get_path(v) for v in self.vertices()]

        return distance, paths

    def bellman_ford(self, s: Vertex):
        distance = {k: float("inf") for k in self.vertices()}
        previous = {k: None for k in self.vertices()}

        distance[s] = 0

        # Relax each edge |V-1| times
        for u in self.vertices():
            for v in self.adjacency(u):
                if distance[v] > distance[u] + self.get_edge_weight(u, v):
                    distance[v] = distance[u] + self.get_edge_weight(u, v)
                    previous[v] = u

        # Detect negative cycle
        for u in self.vertices():
            for v in self.adjacency(u):
                if distance[v] > distance[u] + self.get_edge_weight(u, v):
                    distance[v] = float("-inf")

        return distance

    def add_vertex(self, v: Vertex):
        if v in self:
            return

        self[v] = {}

    def add_vertices(self, *vertices: Vertex):
        for v in vertices:
            self.add_vertex(v)

    def remove_vertex(self, v: Vertex):
        if v not in self:
            return

        self.pop(v)

        for k in self.vertices():
            if v in self[k]:
                self[k].pop(v)

    def has_vertex(self, v: Vertex):
        return v in self

    def add_edge(self, u: Vertex, v: Vertex, w: Weight = 1, symmetric=False):
        for x in [v, u]:
            if x not in self:
                return

        if v in self[u] and u in self[v]:
            return

        self[u][v] = w

        if symmetric:
            self[v][u] = w

    def remove_edge(self, u: Vertex, v: Vertex):
        for x in [v, u]:
            if x not in self:
                return

        if v not in self[u] or u not in self[v]:
            return

        self[u].pop(v)
        self[v].pop(u)

    def has_edge(self, u: Vertex, v: Vertex, symmetric=False):
        return v in self[u] if not symmetric else (v in self[u] and u in self[v])

    def vertices(self):
        return self.keys()

    def adjacency(self, u: Vertex):
        return self[u]

    def get_edge_weight(self, u: Vertex, v: Vertex):
        return self[u][v]
