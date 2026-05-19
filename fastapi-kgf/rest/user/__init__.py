from fastapi import APIRouter

from .profile import router as profile_router
from .settings import router as settings_router

router = APIRouter(prefix="/users")

router.include_router(profile_router)
router.include_router(settings_router)
