from fastapi import APIRouter
from .project_create import router as project_create_router
from .project_delete import router as project_delete_router

router = APIRouter(prefix="/projects")

router.include_router(project_create_router)
router.include_router(project_delete_router)
