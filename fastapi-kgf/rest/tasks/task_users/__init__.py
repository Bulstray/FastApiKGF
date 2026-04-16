from fastapi import APIRouter

from .user_task_endpoints import router as user_tasks_router

router = APIRouter()

router.include_router(user_tasks_router)
