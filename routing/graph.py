"""Graph"""

import random


# wrapper
def normalize(func):
    def wrapper(*args):
        self = args[0]
        if not self._normalized:
            self._normalize()
        return func(*args)

    return wrapper


class Graph:
    def __init__(self, graph_edges):
        self._normalized = None
        self._graph_edges = None
        self._graph = None
        self.update_graph(graph_edges)

    def update_graph(self, graph_edges):
        self._normalized = False
        self._graph_edges = graph_edges

    @normalize
    def modify_with_random(self):
        for vi in self._graph:
            for vj in self._graph[vi]:
                for net in self._graph[vi][vj]:
                    self._graph[vi][vj][net] += random.uniform(-2, 2)

    @normalize
    def merge_multiple_edges(self):
        for vi in self._graph:
            for vj in self._graph[vi]:
                optimal_net = min(self._graph[vi][vj], key=self._graph[vi][vj].get)
                self._graph[vi][vj] = {optimal_net: self._graph[vi][vj][optimal_net]}

    def _normalize(self):
        self._graph = {}
        for edge in self._graph_edges:
            self._normalize_edge(edge[0], edge[1], edge[2], edge[3])
            self._normalize_edge(edge[1], edge[0], edge[2], edge[3])
        self._normalized = True

    def _normalize_edge(self, v_from, v_to, net, weight):
        if v_from not in self._graph:
            self._graph[v_from] = {}
        if v_to not in self._graph[v_from]:
            self._graph[v_from][v_to] = {}
        self._graph[v_from][v_to][net] = weight

    @property
    @normalize
    def graph(self):
        return self._graph
