from fastapi import APIRouter

from .programs import router as program_router

from core.config import settings

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(
    program_router,
    prefix=settings.api.v1.programs,
)
