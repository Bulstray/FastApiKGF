from fastapi import APIRouter

from core.config import settings
from .tenders import router as tenders_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(tenders_router)
