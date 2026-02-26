from fastapi import APIRouter

from .login_page import router as login_page_router
from .login_post import router as login_post_router

router = APIRouter(prefix="/login")

router.include_router(login_page_router)
router.include_router(login_post_router)
