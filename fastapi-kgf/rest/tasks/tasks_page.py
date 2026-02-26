from typing import Annotated

from fastapi import Depends, APIRouter
from starlette.requests import Request

from core.schemas.user import UserRead
from dependencies.providers import get_user_service, get_tasks_service
from dependencies.session_auth import require_auth
from services.task import TasksFilesService
from services.users.service import UserService
from templating.jinja_template import templates


router = APIRouter()


@router.get("/", name="tasks:page")
async def tasks_page(
    request: Request,
    is_auth_user: Annotated[UserRead, Depends(require_auth)],
    user_service: Annotated["UserService", Depends(get_user_service)],
    tasks_service: Annotated["TasksFilesService", Depends(get_tasks_service)],
):
    workers = await user_service.get_all_users()
    tasks = await tasks_service.get_tasks()
    context = {
        "workers": workers,
        "user": is_auth_user,
        "tasks": tasks,
    }

    return templates.TemplateResponse(
        name="tasks.html",
        request=request,
        context=context,
    )
