"""Paths finding algorithm"""


class PathsFindingAlgorithm:
    def __init__(self, graph, n_nodes):
        self.graph = graph
        self.nodes_in_path = n_nodes
        self.paths_n_nodes = {}

    def find_optimal_path(self, v_from, v_to):
        self.paths_n_nodes = {}
        init_params = {
            'path': v_from,
            'length': 0,
            'depth': 1
        }
        self.search(v_from, v_to, init_params)
        optimal_path = min(self.paths_n_nodes, key=self.paths_n_nodes.get)
        return {optimal_path: self.paths_n_nodes[optimal_path]}

    def search(self, v_cur, v_to, params):
        if v_cur == v_to:
            if params['depth'] == self.nodes_in_path:
                self.paths_n_nodes[params['path']] = params['length']
            return

        if params['depth'] < self.nodes_in_path:
            v_next_list = [v for v in self.graph[v_cur]]
            for v_next in v_next_list:
                if v_next not in params['path']:
                    v_next_network = list(self.graph[v_cur][v_next].keys())[0]
                    v_next_params = {
                        'path': params['path'] + f';{v_next_network};{v_next}',
                        'length': params['length'] + self.graph[v_cur][v_next][v_next_network],
                        'depth': params['depth'] + 1
                    }
                    self.search(v_next, v_to, v_next_params)


if __name__ == '__main__':

    my_graph = {'A': {'B': {'local network': 2}, 'C': {'local network': 2}, 'D': {'local network': 3}},
                'B': {'A': {'local network': 2}, 'E': {'local network': 3}},
                'C': {'A': {'local network': 2}, 'D': {'local network': 1}, 'F': {'local network': 4}},
                'D': {'A': {'local network': 3}, 'C': {'local network': 1}, 'E': {'local network': 4},
                      'F': {'local network': 4}, 'G': {'local network': 5}},
                'E': {'B': {'local network': 3}, 'D': {'local network': 4}, 'F': {'local network': 3},
                      'H': {'local network': 2}},
                'F': {'C': {'local network': 4}, 'D': {'local network': 4}, 'E': {'local network': 3},
                      'H': {'local network': 3}},
                'G': {'D': {'local network': 5}, 'H': {'local network': 3}, 'K': {'local network': 2}},
                'H': {'E': {'local network': 2}, 'F': {'local network': 3}, 'G': {'local network': 3},
                      'K': {'local network': 2}},
                'K': {'G': {'local network': 2}, 'H': {'local network': 2}}}
    for vi, v_next in my_graph.items():
        for vj in v_next:
            print(f'{vi} -> {vj}: {my_graph[vi][vj]}', end='\t')
        print()

    alg = PathsFindingAlgorithm(my_graph, 5)
    res = alg.find_optimal_path('A', 'K')
    print(res)
