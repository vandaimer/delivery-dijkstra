import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import async_session
from delivery.views import Healthcheck, Route
from delivery.schemas import RouteSchema, RouteCheapestSchema


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/healthcheck")
def healthcheck(db: Session = Depends(async_session)):
    try:
        return Healthcheck.status(db)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=503,
            detail='I am not live! :(',
        )


@router.post("/route", status_code=201, response_model=RouteSchema,
             tags=["Routes"])
def new_route(input: RouteSchema, db: Session = Depends(async_session)):
    route = Route(db)

    try:
        new_route = route.create(input)
        return new_route
    except ValueError as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail="Error to create a new route.",
        )


@router.get(
    "/route/cheapest/map/{map}/origin/{origin}/destination/{destination}"
    "/truck_autonomy/{truck_autonomy}/gas_price/{gas_price}",
    response_model=RouteCheapestSchema,
    status_code=200, tags=["Routes"])
def route_cheapest(map: str, origin: str, destination: str,
                   truck_autonomy: float, gas_price: float,
                   db: Session = Depends(async_session)):

    route = Route(db)

    try:
        data_input = {
            'map': map,
            'origin': origin,
            'destination': destination,
            'truck_autonomy': truck_autonomy,
            'gas_price': gas_price
        }

        data = route.cheapest(data_input)
        return RouteCheapestSchema(**data)

    except ValueError as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail="Error to retrive the cheapest route.",
        )
