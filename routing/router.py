"""Router"""

import random
from routing.paths_finding_algorithm import PathsFindingAlgorithm


def normalize(func):
    def wrapper(*args):
        self = args[0]
        if not self._normalized:
            self._normalize()
        return func(*args)

    return wrapper


class Graph:
    def __init__(self):
        self._normalized = None
        self._graph_edges = None
        self._graph = None
        self.update_graph()

    def update_graph(self):
        self._normalized = False
        self._graph_edges = self.network_graph()

    def network_graph(self):
        return [
            # from, to, network, weight
            ['A', 'B', 'net1', 2],
            ['A', 'C', 'net1', 2],
            ['A', 'D', 'net1', 3],
            ['B', 'E', 'net1', 3],
            ['C', 'D', 'net1', 1],
            ['C', 'F', 'net1', 4],
            ['D', 'E', 'net1', 4],
            ['D', 'F', 'net1', 4],
            ['D', 'G', 'net1', 5],
            ['E', 'F', 'net1', 3],
            ['E', 'H', 'net1', 2],
            ['F', 'H', 'net1', 3],
            ['G', 'H', 'net1', 3],
            ['G', 'K', 'net1', 2],
            ['H', 'K', 'net1', 2],

            # add some multiple edges
            ['A', 'D', 'net2', 2],
            ['D', 'F', 'net2', 2],
            ['F', 'H', 'net2', 2],
            ['D', 'H', 'net2', 4]
        ]

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


class Router:
    def __init__(self):
        self.net = 'net1'
        self.routes = {}
        self.trans_node_manager = TransitNodeManager()

    def new_route(self, client_id, exit_country):
        graph = Graph()
        graph.modify_with_random()
        graph.merge_multiple_edges()

        alg = PathsFindingAlgorithm(graph.graph, 5)
        route = alg.find_optimal_path(client_id, self.exit_country_node(exit_country))

        self.trans_node_manager.prepare_nodes(route)

        self.routes[client_id] = route

    def exit_country_node(self, country):
        return 'K'


class TransitNodeManager:
    def __init__(self):
        pass

    def prepare_nodes(self, route):
        def config_dict(route_):
            route_list = list(route_.keys())[0].split(';')
            print(route_list)
            setup = {}
            for i in range(0, len(route_list), 4):
                if i == len(route_list) - 1:
                    if route_list[i - 1] not in setup:
                        setup[route_list[i - 1]] = []
                    setup[route_list[i - 1]].append(route_list[i])
                else:
                    if route_list[i + 1] not in setup:
                        setup[route_list[i + 1]] = []
                    setup[route_list[i + 1]].append(route_list[i])
                    setup[route_list[i + 1]].append(route_list[i + 2])
            return setup

        config_nodes = config_dict(route)

    def _prepare(self):
        pass


def print_graph(graph):
    for vi, v_next in graph.items():
        for vj in v_next:
            print(f'{vi} -> {vj}: {graph[vi][vj]}', end='\t')
        print()


if __name__ == '__main__':
    r = Router()
    r.new_route('A', 'some_country')
