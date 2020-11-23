import time

from fastapi import FastAPI, APIRouter

from delivery.api import router as delivery_api


def start():
    app = FastAPI()
    router = APIRouter()

    @router.get("/{path:path}", status_code=501)
    def not_implement(path):
        return {
            'path': f"/{path}",
            'status': 'notImplemented',
            'now': time.time(),
        }

    app.include_router(delivery_api, prefix="/api/v1")
    app.include_router(router)

    return app
