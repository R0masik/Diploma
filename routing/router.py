"""Router"""

from time import time, sleep
from random import choice
from threading import Thread
from routing.graph import Graph
from routing.transit_node_man import TransitNodeManager
from routing.path_finding_algorithm import PathFindingAlgorithm


class Router:
    def __init__(self, n_nodes=4, t_route=600):
        self.net = 'net1'
        self.net_graph = None
        self.routes = {}
        self.nodes_number = n_nodes
        self.route_lifetime = t_route
        self.trans_node_manager = TransitNodeManager()

        thread = Thread(target=self.tracking_routes_lifetimes)
        # thread.daemon = True
        thread.start()

    def new_route(self, net_graph, client_id, exit_country_dict):
        if isinstance(self.nodes_number, int):
            if self.nodes_number > 0:
                if isinstance(net_graph, list):
                    self.net_graph = net_graph
                    graph = Graph(net_graph)
                    graph.modify_with_random()
                    graph.merge_multiple_edges()

                    alg = PathFindingAlgorithm(graph.graph, self.nodes_number)
                    route = alg.find_optimal_path(client_id, self._exit_country_node(exit_country_dict))

                    if route:
                        self.trans_node_manager.prepare_nodes(route)
                        self.routes[client_id] = {
                            'route': route,
                            'death': time() + self.route_lifetime,
                            'exit_country_dict': exit_country_dict
                        }
                else:
                    return 'Net graph must be given as a list'
            else:
                return 'Number of nodes must be greater than 0'
        else:
            return 'Number of nodes must be an integer'

    def _exit_country_node(self, country_dict):
        country = tuple(country_dict.keys())[0]
        return choice(country_dict[country])

    def tracking_routes_lifetimes(self):
        while True:
            if self.routes:
                for client_id, route_info in self.routes.items():
                    print(f'Check client {client_id}')
                    if time() >= route_info['death']:
                        self.new_route(self.net_graph, client_id, route_info['exit_country_dict'])
            sleep(5)


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

        ['A', 'D', 'net2', 2],
        ['D', 'F', 'net2', 2],
        ['F', 'H', 'net2', 2],
        ['D', 'E', 'net2', 4],
        ['K', 'H', 'net2', 3],
        ['G', 'F', 'net2', 2],
        ['C', 'E', 'net2', 5],
        ['C', 'K', 'net2', 4],
        ['E', 'H', 'net2', 3],
        ['D', 'B', 'net2', 2],
        ['F', 'K', 'net2', 4],
        ['B', 'D', 'net2', 1],
        ['A', 'H', 'net2', 3],

        ['A', 'D', 'net3', 3],
        ['D', 'F', 'net3', 2],
        ['F', 'H', 'net3', 4],
        ['D', 'E', 'net3', 3],
        ['K', 'H', 'net3', 2],
        ['G', 'F', 'net3', 1],
        ['C', 'E', 'net3', 4],
        ['C', 'K', 'net3', 3],
        ['E', 'H', 'net3', 2],
        ['D', 'B', 'net3', 3],
        ['F', 'K', 'net3', 1],
        ['B', 'D', 'net3', 3],
        ['A', 'H', 'net3', 3],
    ]
    exit_country_d = {'some_country': ['K', 'G', 'C']}

    r = Router()
    a = time()
    for i in range(500):
        in_nodes_list = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K')
        r.new_route(my_graph, choice(in_nodes_list), exit_country_d)
        print(r.routes)
    print(time() - a)
