"""Router"""

from routing.graph import Graph
from routing.transit_node_man import TransitNodeManager
from routing.path_finding_algorithm import PathFindingAlgorithm


class Router:
    def __init__(self, n_nodes=4):
        self.net = 'net1'
        self.routes = {}
        self.nodes_number = n_nodes
        self.trans_node_manager = TransitNodeManager()

    def new_route(self, net_graph, client_id, exit_country_dict):
        graph = Graph(net_graph)
        graph.modify_with_random()
        graph.merge_multiple_edges()

        alg = PathFindingAlgorithm(graph.graph, self.nodes_number)
        route = alg.find_optimal_path(client_id, self._exit_country_node(exit_country_dict))

        if route:
            self.trans_node_manager.prepare_nodes(route)
            self.routes[client_id] = route
            print(route)

    def _exit_country_node(self, country_dict):
        return 'K'


def print_graph(graph):
    for vi, v_next in graph.items():
        for vj in v_next:
            print(f'{vi} -> {vj}: {graph[vi][vj]}', end='\t')
        print()


if __name__ == '__main__':
    my_graph = [
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
    r = Router(4)
    r.new_route(my_graph, 'A', {'some_country': ['K', 'G', 'C']})
