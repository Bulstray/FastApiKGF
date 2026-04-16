from fastapi import APIRouter

from .chat import router as chat_router
from .notifications import router as notification_router
from .task_users import router as task_users_router
from .create_task import router as create_task_router
from .delete_task import router as delete_task_router
from .download_file import router as download_file_router
from .tasks_page import router as tasks_page_router

router = APIRouter(prefix="/tasks")

router.include_router(create_task_router)
router.include_router(delete_task_router)
router.include_router(download_file_router)
router.include_router(tasks_page_router)
router.include_router(chat_router)
router.include_router(notification_router)
router.include_router(task_users_router)
