from fastapi import APIRouter

from .create_task import router as create_task_router
from .delete_task import router as delete_task_router
from .download_file import router as download_file_router
from .tasks_page import router as tasks_page_router
from .update_task import router as update_task_router
from .chat_task import router as chat_task_router


router = APIRouter(prefix="/tasks")

router.include_router(create_task_router)
router.include_router(delete_task_router)
router.include_router(download_file_router)
router.include_router(tasks_page_router)
router.include_router(update_task_router)

router.include_router(chat_task_router)
