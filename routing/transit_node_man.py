"""Transit node manager"""


class TransitNodeManager:
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
