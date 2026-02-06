from fastapi import APIRouter
from core.config import settings
from .fastapi_users_router import fastapi_users_router
from api.dependencies.authentication.backend import authentication_backend

from core.schemas import UserCreate, UserRead

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users_router.get_auth_router(
        authentication_backend,
    ),
)

# /register
router.include_router(
    router=fastapi_users_router.get_register_router(
        UserRead,
        UserCreate,
    )
)
