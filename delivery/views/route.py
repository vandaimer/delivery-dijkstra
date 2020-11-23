from delivery.models import Route as RouteModel


class Route:
    @staticmethod
    def create(route, db):
        new_route = RouteModel(**route.dict())
        db.add(new_route)
        db.commit()

        return route
