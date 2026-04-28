from fastapi import APIRouter

from .page import router as project_page_router

router = APIRouter(
    prefix="/projects",
)

router.include_router(project_page_router)
