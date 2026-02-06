from fastapi import APIRouter
from core.config import settings
from .fastapi_users_router import fastapi_users_router
from api.dependencies.authentication.backend import authentication_backend

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

router.include_router(
    router=fastapi_users_router.get_auth_router(
        authentication_backend,
    ),
)
