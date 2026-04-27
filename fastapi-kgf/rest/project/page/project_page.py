import datetime
from typing import Annotated, Any

from fastapi import Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter

from core.schemas.user import UserRead
from dependencies.message import get_message_service
from dependencies.projects import get_project_service
from dependencies.providers import get_user_service, get_tasks_service
from dependencies.session_auth import get_current_user
from services.messages.message_service import MessageManager
from services.projects.service import ProjectService
from services.task import TasksFilesService
from services.users.service import UserService
from templating.jinja_template import templates

router = APIRouter()


async def _build_context(
    project_id: int,
    user: Annotated[UserRead, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    tasks_service: Annotated[TasksFilesService, Depends(get_tasks_service)],
    message_service: Annotated[MessageManager, Depends(get_message_service)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> dict[str, Any]:
    count_unread_message = await message_service.get_unread_message(user.id)
    workers_list = await user_service.get_all()
    tasks_for_users = await tasks_service.get_user_tasks_by_project_id(
        project_id, user.id
    )
    projects = await project_service.get_all()
    project = await project_service.get_by_id(project_id)

    return {
        "workers": workers_list,
        "user": user,
        "tasks": tasks_for_users,
        "unread_messages": count_unread_message,
        "projects": projects,
        "project_id": project_id,
        "project": project,
        "today": datetime.date.today(),
    }


@router.get(
    "/{project_id}",
    name="project:page",
    response_model=None,
)
async def tasks_page(
    request: Request,
    context: Annotated[dict[str, Any], Depends(_build_context)],
) -> HTMLResponse | RedirectResponse:

    if not context.get("project"):
        return RedirectResponse(
            url="/",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return templates.TemplateResponse(
        name="tasks.html",
        request=request,
        context=context,
    )
