from delivery.models import Route as RouteModel


class Route:
    @staticmethod
    def create(route, db):
        exists = db.query(
            db.query(RouteModel).filter_by(**route.dict()).exists(),
        ).scalar()

        if exists:
            raise ValueError('This route already exists.')

        new_route = RouteModel(**route.dict())
        db.add(new_route)
        db.commit()

        return route
