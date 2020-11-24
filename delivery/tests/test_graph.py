from delivery.graph import DeliveryGraph


class TestDeliverGraph:
    def setup_method(self):
        self.graph = DeliveryGraph()
        self.first_element = 'A'
        self.second_element = 'B'
        self.weight = 10

        self.mock = [
            (self.first_element,
             self.second_element,
             self.weight,),
        ]

        self.graph.populate_graph(self.mock)

    def test_populate_graph(self):
        mock = self.mock
        self.graph.populate_graph(mock)

        node = list(self.graph.graph.get_nodes())[0]

        assert node == self.first_element

    def test_shortest_path(self):
        third_element = 'C'
        fourth_element = 'D'

        self.mock.append((self.second_element, third_element, 5))
        self.mock.append((self.first_element, fourth_element, 10))
        self.mock.append((fourth_element, third_element, 4))

        self.graph.populate_graph(self.mock)

        shortest_path = self.graph.shortest_path(
            self.first_element,
            third_element,
        )

        assert shortest_path == [
            self.first_element,
            fourth_element,
            third_element,
        ]

    def test_shortest_distance(self):
        third_element = 'C'
        fourth_element = 'D'
        fourth_third_weight = 4

        self.mock.append((self.second_element, third_element, 5))
        self.mock.append((self.first_element, fourth_element, 10))
        self.mock.append((fourth_element, third_element, fourth_third_weight))

        self.graph.populate_graph(self.mock)

        shortest_distance = self.graph.shortest_distance(
            self.first_element,
            third_element,
        )
        total_distance = self.weight + fourth_third_weight

        assert shortest_distance == total_distance
