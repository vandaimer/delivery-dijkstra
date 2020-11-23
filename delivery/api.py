import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import async_session
from delivery.views import Healthcheck


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
