"""Path with N nodes"""


class Algorithm:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = self.graph.keys()
        self.n_nodes = 5
        self.paths = {}

    def find_paths(self, v_from, v_to):
        self.paths = {}
        init_params = {
            'path': v_from,
            'length': 0,
            'depth': 1
        }
        self.find_path(v_from, v_to, init_params)
        return self.paths

    def find_path(self, v_cur, v_to, params):
        if v_cur == v_to:
            if params['depth'] == self.n_nodes:
                self.paths[params['path']] = params['length']
            return

        if params['depth'] < self.n_nodes:
            v_next_list = [v for v in self.vertices if self.graph[v_cur][v]]
            for v_next in v_next_list:
                if v_next not in params['path']:
                    v_next_params = {
                        'path': params['path'] + v_next,
                        'length': params['length'] + self.graph[v_cur][v_next],
                        'depth': params['depth'] + 1
                    }
                    self.find_path(v_next, v_to, v_next_params)


if __name__ == '__main__':
    v_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K']
    list_e_list = [
        [None, 2, 2, 3, None, None, None, None, None],
        [2, None, None, None, 3, None, None, None, None],
        [2, None, None, 1, None, 4, None, None, None],
        [3, None, 1, None, 4, 4, 5, None, None],
        [None, 3, None, 4, None, 3, None, 2, None],
        [None, None, 4, 4, 3, None, None, 3, None],
        [None, None, None, 5, None, None, None, 3, 2],
        [None, None, None, None, 2, 3, 3, None, 2],
        [None, None, None, None, None, None, 2, 2, None]
    ]
    my_graph = dict(zip(v_list, [dict(zip(v_list, e_list)) for e_list in list_e_list]))
    for vi in my_graph:
        for vj in my_graph:
            print_str = f'{vj} -> {vi}: {my_graph[vi][vj]}'
            if my_graph[vi][vj] is not None:
                print_str += '\t'
            print(print_str, end='\t')
        print()

    alg = Algorithm(my_graph)
    for path, length in alg.find_paths('A', 'K').items():
        print(f'{path} = {length}')
