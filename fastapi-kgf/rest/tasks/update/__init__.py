from fastapi import APIRouter

from .update_status_websocket import router as update_status_router

router = APIRouter()

router.include_router(update_status_router)
