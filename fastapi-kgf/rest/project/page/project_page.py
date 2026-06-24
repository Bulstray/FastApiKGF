import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from core.schemas.user import UserRead
from dependencies import (
    TaskFactory,
    TaskMessageFactory,
)
from dependencies.session_auth import get_current_user
from services import (
    UserService,
)
from templating.jinja_template import templates

from storage.db.crud_user import get_all_users
from storage.db.crud_project import get_all_projects, get_project_by_id

from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def _get_user_and_user_service(
    user: Annotated[UserRead, Depends(get_current_user)],
) -> UserRead:
    return user


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
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> dict[str, Any]:
    user = user_and_user_service
    count_unread_message = await message_service.get_unread_message(user.id)
    tasks_for_users = await tasks_service.get_user_tasks_by_project_id(
        project_id,
        user.id,
    )

    return {
        "project_id": project_id,
        "workers": await get_all_users(session),
        "user": user,
        "tasks": tasks_for_users,
        "unread_messages": count_unread_message,
        "projects": await get_all_projects(session),
        "project": await get_project_by_id(session, project_id),
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
