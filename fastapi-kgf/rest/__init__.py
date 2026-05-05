from fastapi import APIRouter, Depends

from dependencies.session_auth import get_cookie_websocket, require_auth

from .auth import router as auth_router
from .home import router as main_router
from .programs import router as programs_router
from .project import router as project_router
from .tasks import router as tasks_router
from .tasks.chat.chat_websocket import router as chat_websocket_router
from .tasks.notifications.notifications_websocket import (
    router as notification_websocket_router,
)
from .tasks.update.update_status_websocket import router as update_task
from .tenders import router as tenders_router
from .user import router as user_router

router = APIRouter(
    include_in_schema=False,
)

router_rest = APIRouter(dependencies=[Depends(require_auth)])
router_rest.include_router(main_router)
router_rest.include_router(programs_router)
router_rest.include_router(tenders_router)
router_rest.include_router(tasks_router)
router_rest.include_router(project_router)
router_rest.include_router(user_router)

router.include_router(router_rest)
router.include_router(auth_router)

router_websocket = APIRouter(
    dependencies=[Depends(get_cookie_websocket)],
    prefix="/tasks",
)
router_websocket.include_router(chat_websocket_router)
router_websocket.include_router(update_task)
router_websocket.include_router(notification_websocket_router)

router.include_router(router_websocket)
