from fastapi import APIRouter

from core.config import settings
from api.api_v1.fastapi_users_router import fastapi_users_router
from core.schemas import UserRead, UserUpdate

router = APIRouter(prefix=settings.api.v1.users, tags=["Users"])

# /me
# /id
router.include_router(
    router=fastapi_users_router.get_users_router(
        UserRead,
        UserUpdate,
    )
)
