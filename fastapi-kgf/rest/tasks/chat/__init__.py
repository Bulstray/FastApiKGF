from fastapi import APIRouter

from .chat_endpoint import router as chat_router

router = APIRouter()

router.include_router(chat_router)
