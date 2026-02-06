from fastapi import APIRouter, Depends

from core.config import settings
from .auth import router as auth_router

from .programs import router as program_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    program_router,
    prefix=settings.api.v1.programs,
)

router.include_router(
    auth_router,
)
