from fastapi import APIRouter

from .auth import router as auth_router
from .home_router import router as main_router
from .programs import router as programs_router
from .tenders import router as tenders_router
from .tasks import router as tasks_router
from .test import router as test_router

router = APIRouter(include_in_schema=False)

router.include_router(main_router)
router.include_router(programs_router)
router.include_router(tenders_router)
router.include_router(auth_router)
router.include_router(tasks_router)
router.include_router(test_router)
