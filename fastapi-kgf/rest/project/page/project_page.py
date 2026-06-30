import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from core.schemas.user import UserRead

from dependencies.session_auth import get_current_user
from templating.jinja_template import templates


from storage.db import crud_project, crud_user, crud_tasks, crud_message

from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def _build_context(
    project_id: int,
    user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> dict[str, Any]:

    return {
        "project_id": project_id,
        "workers": await crud_user.get_all_users(session),
        "user": user,
        "tasks": await crud_tasks.get_tasks_by_project_id(
            session,
            project_id,
            user.id,
        ),
        "unread_messages": await crud_message.get_unread_message(
            session,
            user.id,
        ),
        "projects": await crud_project.get_all_projects(session),
        "project": await crud_project.get_project_by_id(session, project_id),
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
