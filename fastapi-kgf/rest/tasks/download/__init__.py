from fastapi import APIRouter

from .download_endpoints import router as download_router

router = APIRouter()

router.include_router(download_router)
