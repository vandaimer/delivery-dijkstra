from delivery.models import Route as RouteModel
from delivery.graph import DeliveryGraph


class Route:
    @staticmethod
    def create(route, db):
        valid_input = Route.validate_input(route, db)

        if valid_input:
            raise ValueError('This route already exists.')

        new_route = RouteModel(**route.dict())
        db.add(new_route)
        db.commit()

        return route

    @staticmethod
    def cheapest(data, db):

        routes = db.query(RouteModel).filter_by(map=data['map']).all()
        routes = [
            (route.origin, route.destination, route.distance)
            for route in routes
        ]

        graph = DeliveryGraph(routes)

        shortest_distance = graph.shortest_distance(
            data['origin'],
            data['destination'],
        )
        shortest_path = graph.shortest_path(
            data['origin'],
            data['destination'],
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

    @staticmethod
    def calculate_expenses(gas_price, truck_autonomy, distance):
        return (distance/truck_autonomy) * gas_price

    @staticmethod
    def validate_input(route, db):
        unique_route = route.dict()
        del unique_route['distance']

        return db.query(
            db.query(RouteModel).filter_by(**unique_route).exists(),
        ).scalar()
