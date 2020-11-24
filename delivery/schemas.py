from typing import List

from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .models import Route


RouteSchema = sqlalchemy_to_pydantic(Route, exclude={"id"})


class RouteCheapestSchema(BaseModel):
    route: List[str]
    cost: float
