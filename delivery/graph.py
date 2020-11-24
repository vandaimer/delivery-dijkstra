from dijkstra import DijkstraSPF, Graph


class DeliveryGraph:
    """Graph lib wrapper

    Parameters
    data (list(tuple)): The data should be a list of tuple.
    Each tuple should have 3 values.
    The first value should be the node A
    The second value should be the node B
    The last value should be the weight between node A and node B

    exemple:
        data = [('NodeA', 'Node B', 10.5)]

    """
    def __init__(self, data):
        self.graph = Graph()
        self._populate_graph(data)

    def _populate_graph(self, data):
        for item in data:
            self.graph.add_edge(item[0], item[1], item[2])

    def shortest_path(self, nodeA, nodeB):
        dijkstra = DijkstraSPF(self.graph, nodeA)
        return dijkstra.get_path(nodeB)

    def shortest_distance(self, nodeA, nodeB):
        dijkstra = DijkstraSPF(self.graph, nodeA)
        return dijkstra.get_distance(nodeB)
