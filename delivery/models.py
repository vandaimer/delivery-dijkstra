from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from db import BaseSQLAlchemy


class Route(BaseSQLAlchemy):
    id = Column(Integer, primary_key=True)
    map = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)

    @validates('map', 'origin', 'destination')
    def validate_empty_fields(self, key, value):
        if value == '' or value.strip() == '':
            raise ValueError(f"Field {key} must be not empty.")
        return value
