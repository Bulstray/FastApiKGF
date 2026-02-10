from fastapi import APIRouter, Depends

from core.config import settings
from dependencies.auth_admin import validate_basic_auth

from .programs import router as program_router
from .user import router as user_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[
        Depends(validate_basic_auth),
    ],
)

router.include_router(
    program_router,
    prefix=settings.api.v1.programs,
)

router.include_router(
    user_router,
    prefix=settings.api.v1.users,
)
