from fastapi import APIRouter

from core.config import settings

from .programs import router as program_router
from .users import router as users_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(
    program_router,
    prefix=settings.api.v1.programs,
)

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)
