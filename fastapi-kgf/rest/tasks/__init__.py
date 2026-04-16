from fastapi import APIRouter
from .chat import router as chat_router
from .create import router as create_router
from .download import router as download_router
from .task_users import router as task_users_router


router = APIRouter(prefix="/tasks")

router.include_router(chat_router)
router.include_router(create_router)
router.include_router(download_router)
router.include_router(task_users_router)
