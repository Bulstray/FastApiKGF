from fastapi import APIRouter

from .create_project_endpoints import router as create_project_router


router = APIRouter()

router.include_router(create_project_router)
