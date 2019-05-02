"""Dijkstra"""

from pprint import pprint


class DijkstraAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = self.graph.keys()

    def shortest_way(self, v_from, v_to):
        d = {}
        used = {}
        for v in self.vertices:
            d[v] = float('inf')
            used[v] = False

        d[v_from] = 0

        for i in self.vertices:
            v_min = None
            for j in self.vertices:
                if not used[j] and (v_min is None or d[j] < d[v_min]):
                    v_min = j

            if d[v_min] == float('inf'):
                break

            used[v_min] = True

            for v_next in [v for v in self.vertices if self.graph[v_min][v]]:
                if d[v_min] + self.graph[v_min][v_next] < d[v_next]:
                    d[v_next] = d[v_min] + self.graph[v_min][v_next]

            print(d)
            print(used)


if __name__ == '__main__':
    v_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    list_e_list = [
        [None, 5, None, 17, 7, None, None],
        [5, None, 4, None, None, None, None],
        [None, 4, None, 3, None, None, None],
        [17, None, 3, None, 3, None, 8],
        [7, None, None, 3, None, 5, None],
        [None, None, None, None, 5, None, 10],
        [None, None, None, 8, None, 10, None]
    ]
    my_graph = dict(zip(v_list, [dict(zip(v_list, e_list)) for e_list in list_e_list]))
    for vi in my_graph:
        for vj in my_graph:
            print_str = f'{vj} -> {vi}: {my_graph[vi][vj]}'
            if my_graph[vi][vj] is not None:
                print_str += '\t'
            print(print_str, end='\t')
        print()

    alg = DijkstraAlgorithm(my_graph)
    print(alg.shortest_way('a', 'g'))
