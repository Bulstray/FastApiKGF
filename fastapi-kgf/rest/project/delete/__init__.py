from fastapi import APIRouter

from .delete_project_endpoints import router as router_delete_project

router = APIRouter()

router.include_router(router_delete_project)
