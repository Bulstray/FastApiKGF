from fastapi import APIRouter

from .notifications_endpoint import router as notification_router

router = APIRouter()

router.include_router(notification_router)
