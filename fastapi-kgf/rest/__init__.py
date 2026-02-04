from fastapi import APIRouter

from .main_views import router as main_router
from .programs import router as programs_router
from .tenders import router as tenders_router

router = APIRouter()

router.include_router(main_router)
router.include_router(programs_router)
router.include_router(tenders_router)
