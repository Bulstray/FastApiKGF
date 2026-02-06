from fastapi import APIRouter, Depends

from core.config import settings
from dependencies.auth import admin_auth_dependency
from .auth import router as auth_router

from .programs import router as program_router
from .users import router as users_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[
        # Depends(admin_auth_dependency),
    ],
)

router.include_router(
    program_router,
    prefix=settings.api.v1.programs,
)

router.include_router(
    auth_router,
)

# router.include_router(
#     users_router,
#     prefix=settings.api.v1.users,
# )
