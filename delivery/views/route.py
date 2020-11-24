from delivery.models import Route as RouteModel
from delivery.graph import DeliveryGraph


class Route:
    def __init__(self, db):
        self.db = db

    def create(self, route):
        valid_input = self.validate_input(route)

        if valid_input is not None:
            raise ValueError('This route already exists.')

        new_route = RouteModel(**route.dict())
        self.db.add(new_route)
        self.db.commit()

        return route

    def cheapest(self, data):
        self.validate_cheapest_input(data)

        routes = self.db.query(RouteModel).filter(RouteModel.map == data['map']).all()
        routes = [
            (route.origin, route.destination, route.distance)
            for route in routes
        ]

        graph = DeliveryGraph()
        graph.populate_graph(routes)

        origin = data['origin']
        destination = data['destination']

        shortest_distance = graph.shortest_distance(
            origin,
            destination,
        )
        shortest_path = graph.shortest_path(
            origin,
            destination,
        )

        cost = Route.calculate_expenses(
            data['gas_price'],
            data['truck_autonomy'],
            shortest_distance,
        )

        return {
            'route': shortest_path,
            'cost': cost,
        }

    def validate_cheapest_input(self, data):
        map = data['map']

        self.validate_map(map)
        self.validate_origin(map, data['origin'])
        self.validate_destination(map, data['destination'])

    def validate_destination(self, map, destination):
        routes = self.db.query(RouteModel.id).filter(
            RouteModel.map == map,
            RouteModel.destination == destination,
        ).count()

        if routes == 0:
            raise ValueError('This destination on this map does not exists.')

    def validate_origin(self, map, origin):
        routes = self.db.query(RouteModel.id).filter(
            RouteModel.map == map,
            RouteModel.origin == origin,
        ).count()

        if routes == 0:
            raise ValueError('This origin on this map does not exists.')

    def validate_map(self, map):
        routes = self.db.query(RouteModel.id).filter(RouteModel.map == map).count()

        if routes == 0:
            raise ValueError('This map does not exists.')

    @staticmethod
    def calculate_expenses(gas_price, truck_autonomy, distance):
        return (distance/truck_autonomy) * gas_price

    def validate_input(self, route):
        return self.db.query(RouteModel.id).filter(
            RouteModel.map == route.map,
            RouteModel.origin == route.origin,
            RouteModel.destination == route.destination,
        ).one_or_none()
