import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from core.schemas.user import UserRead
from dependencies import ProjectFactory, TaskFactory, TaskMessageFactory
from dependencies.session_auth import get_current_user
from services import (
    MessageManager,
    UserService,
)
from dependencies import UserServiceFactory
from templating.jinja_template import templates

router = APIRouter()


async def _get_user_and_user_service(
    user: Annotated[UserRead, Depends(get_current_user)],
    user_service: Annotated[
        UserServiceFactory,
        Depends(UserServiceFactory),
    ],
) -> tuple[UserRead, UserService]:
    return user, user_service


async def _build_context(
    project_id: int,
    user_and_user_service: Annotated[
        tuple[UserRead, UserService],
        Depends(_get_user_and_user_service),
    ],
    tasks_service: Annotated[
        TaskFactory,
        Depends(TaskFactory),
    ],
    message_service: Annotated[
        TaskMessageFactory,
        Depends(TaskMessageFactory),
    ],
    project_service: Annotated[
        ProjectFactory,
        Depends(ProjectFactory),
    ],
) -> dict[str, Any]:
    user, user_service = user_and_user_service
    count_unread_message = await message_service.get_unread_message(user.id)
    workers_list = await user_service.get_all()
    tasks_for_users = await tasks_service.get_user_tasks_by_project_id(
        project_id,
        user.id,
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
        "today": datetime.datetime.now(tz=datetime.UTC).date(),
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
