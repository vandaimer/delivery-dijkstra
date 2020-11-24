from delivery.models import Route as RouteModel


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
    def validate_input(route, db):
        unique_route = route.dict()
        del unique_route['distance']

        return db.query(
            db.query(RouteModel).filter_by(**unique_route).exists(),
        ).scalar()
