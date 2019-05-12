"""Router"""

from routing.graph import Graph
from routing.paths_finding_algorithm import PathsFindingAlgorithm


class Router:
    def __init__(self):
        self.net = 'net1'
        self.routes = {}
        self.trans_node_manager = TransitNodeManager()

    def new_route(self, client_id, exit_country):
        graph = Graph()
        graph.modify_with_random()
        graph.merge_multiple_edges()

        alg = PathsFindingAlgorithm(graph.graph, 4)
        route = alg.find_optimal_path(client_id, self.exit_country_node(exit_country))

        self.trans_node_manager.prepare_nodes(route)

        self.routes[client_id] = route

    def exit_country_node(self, country):
        return 'K'


class TransitNodeManager:
    def __init__(self):
        pass

    def prepare_nodes(self, route):
        def config_nodes_dict(route_):
            route_list = list(route_.keys())[0].split(';')
            setup = {}
            for i in range(1, len(route_list), 2):
                if route_list[i] not in setup:
                    setup[route_list[i]] = []
                setup[route_list[i]].append((route_list[i - 1], route_list[i + 1]))
            return setup

        config_nodes = config_nodes_dict(route)
        for net, nodes in config_nodes.items():
            self._prepare(net, nodes)

    def _prepare(self, net, nodes_list):
        pass


def print_graph(graph):
    for vi, v_next in graph.items():
        for vj in v_next:
            print(f'{vi} -> {vj}: {graph[vi][vj]}', end='\t')
        print()


if __name__ == '__main__':
    r = Router()
    r.new_route('A', 'some_country')
