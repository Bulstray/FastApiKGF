import datetime
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from dependencies.message import get_message_service
from dependencies.providers import get_tasks_service, get_user_service
from dependencies.session_auth import require_auth
from templating.jinja_template import templates

if TYPE_CHECKING:
    from core.schemas.user import UserRead
    from services.messages.message_service import MessageManager
    from services.task import TasksFilesService
    from services.users.service import UserService

router = APIRouter()


@router.get("/", name="tasks:page")
async def tasks_page(
    request: Request,
    is_auth_user: Annotated["UserRead", Depends(require_auth)],
    user_service: Annotated["UserService", Depends(get_user_service)],
    tasks_service: Annotated["TasksFilesService", Depends(get_tasks_service)],
    message_service: Annotated["MessageManager", Depends(get_message_service)],
) -> HTMLResponse:
    unread_messages = await message_service.get_unread_message(is_auth_user.id)
    workers = await user_service.get_all_users()
    tasks = await tasks_service.get_tasks()

    context = {
        "workers": workers,
        "user": is_auth_user,
        "tasks": tasks,
        "unread_messages": unread_messages,
        "today": datetime.date.today(),
    }

    return templates.TemplateResponse(
        name="tasks.html",
        request=request,
        context=context,
    )
