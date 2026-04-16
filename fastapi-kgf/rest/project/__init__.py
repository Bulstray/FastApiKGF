from fastapi import APIRouter
from .create import router as router_create_project
from .delete import router as router_delete_project
from .page import router as project_page_router


router = APIRouter(
    prefix="/projects",
)

router.include_router(router_create_project)
router.include_router(router_delete_project)
router.include_router(project_page_router)
