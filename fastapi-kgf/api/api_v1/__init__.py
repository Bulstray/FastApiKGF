from fastapi import APIRouter

from core.config import settings

from .programs import router as programs_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

programs_router.include_router(
    programs_router,
    prefix=settings.api.v1.programs,
)
