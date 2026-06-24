from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates

from storage.db import crud_project, crud_programs
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

router = APIRouter()


@router.get("/", name="programs:page")
async def programs_page(
    request: Request,
    is_authenticated: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> HTMLResponse:
    """Render programs listing page."""

    return templates.TemplateResponse(
        request=request,
        name="programs.html",
        context={
            "programs": await crud_programs.get_all_programs(session),
            "is_authenticated": is_authenticated,
            "projects": await crud_project.get_all_projects(session),
        },
    )
