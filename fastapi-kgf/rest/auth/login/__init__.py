from fastapi import APIRouter

from .login_page import router as login_page_router
from .login_post import router as login_post_router

from core.config import settings

router = APIRouter(prefix=settings.api.v1.login)

router.include_router(login_page_router)
router.include_router(login_post_router)
