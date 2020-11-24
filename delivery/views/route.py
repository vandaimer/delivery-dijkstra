from delivery.models import Route as RouteModel
from delivery.graph import DeliveryGraph


class Route:
    def __init__(self, db):
        self.db = db

    def create(self, route):
        valid_input = self.validate_input(route)

        if valid_input:
            raise ValueError('This route already exists.')

        new_route = RouteModel(**route.dict())
        self.db.add(new_route)
        self.db.commit()

        return route

    def cheapest(self, data):
        self.validate_cheapest_input(data)

        routes = self.db.query(RouteModel).filter_by(map=data['map']).all()
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

        cost = self.calculate_expenses(
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
        exists = self.db.query(
            self.db.query(RouteModel).filter_by(
                map=map,
                destination=destination,
            ).exists(),
        ).scalar()

        if exists is False:
            raise ValueError('This destination on this map does not exists.')

    def validate_origin(self, map, origin):
        exists = self.db.query(
            self.db.query(RouteModel).filter_by(
                map=map,
                origin=origin,
            ).exists(),
        ).scalar()

        if exists is False:
            raise ValueError('This origin on this map does not exists.')

    def validate_map(self, map):
        exists = self.db.query(
            self.db.query(RouteModel).filter_by(map=map).exists(),
        ).scalar()

        if exists is False:
            raise ValueError('This map does not exists.')

    def calculate_expenses(self, gas_price, truck_autonomy, distance):
        return (distance/truck_autonomy) * gas_price

    def validate_input(self, route):
        unique_route = route.dict()
        del unique_route['distance']

        return self.db.query(
            self.db.query(RouteModel).filter_by(**unique_route).exists(),
        ).scalar()
