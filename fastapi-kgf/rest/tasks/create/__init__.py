from fastapi import APIRouter

from .create_task_endpoints import router as create_task

router = APIRouter()

router.include_router(create_task)
