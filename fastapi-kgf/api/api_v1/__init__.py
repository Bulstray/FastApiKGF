from fastapi import APIRouter, Depends

from core.config import settings
from dependencies.auth_admin import validate_basic_auth_admin

from .programs import router as program_router
from .users import router as users_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[
        Depends(validate_basic_auth_admin),
    ],
)

router.include_router(
    program_router,
    prefix=settings.api.v1.programs,
)

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)
