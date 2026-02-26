from fastapi import APIRouter, Depends

from dependencies.session_auth import require_auth

from .tenders_page import router as page_router
from .tenders_search import router as search_router

router = APIRouter(
    prefix="/tenders",
    dependencies=[Depends(require_auth)],
)


router.include_router(page_router)
router.include_router(search_router)
