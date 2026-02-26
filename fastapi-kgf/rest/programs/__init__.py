from fastapi import APIRouter

from .download import router as download_router
from .programs_page import router as programs_page_router

router = APIRouter(prefix="/programs")

router.include_router(programs_page_router)
router.include_router(download_router)
