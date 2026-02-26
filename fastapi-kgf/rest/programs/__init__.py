from fastapi import APIRouter, Depends

from .download import router as download_router
from .programs_page import router as programs_page_router

from dependencies.session_auth import require_auth


router = APIRouter(prefix="/programs")

router.include_router(programs_page_router)
router.include_router(download_router)
