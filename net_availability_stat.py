"""Net availability stat"""


class NetAvailabilityStat:
    def __init__(self, net0, net1, net2):
        self.stat = {
            net0: {},
            net1: {},
            net2: {}
        }

    def get_client_ids(self):
        pass

    def collect_ping(self):
        pass

    def calculate_average(self, node_id):
        pass
