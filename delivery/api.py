import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db import async_session
from delivery.views import Healthcheck, Route
from delivery.schemas import RouteSchema


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


@router.post("/route", status_code=201, response_model=RouteSchema, tags=["Routes"])
def new_route(route: RouteSchema, db: Session = Depends(async_session)):
    try:
        new_route = Route.create(route, db)
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
