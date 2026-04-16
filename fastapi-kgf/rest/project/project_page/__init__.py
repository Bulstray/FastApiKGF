from fastapi import APIRouter

from .project_page import router as project_routes

router = APIRouter()


router.include_router(project_routes)
