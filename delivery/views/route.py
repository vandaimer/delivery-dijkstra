from delivery.models import Route as RouteModel


class Route:
    @staticmethod
    def create(route, db):
        exists = Route.validate_route_exists(route)

        if valid_input:
            raise ValueError('This route already exists.')

        new_route = RouteModel(**route.dict())
        db.add(new_route)
        db.commit()

        return route

    @staticmethod
    def validate_route_exists(route):
        unique_route = route.dict().copy()
        del unique_route['distance']

        return db.query(
            db.query(RouteModel).filter_by(**unique_route).exists(),
        ).scalar()

