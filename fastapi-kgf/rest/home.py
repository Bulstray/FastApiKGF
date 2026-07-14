from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates
from core.models import db_helper
from storage.db import crud_project
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", name="home:page")
async def home(
    request: Request,
    is_authenticated: Annotated[
        UserRead | None,
        Depends(get_current_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "is_authenticated": is_authenticated,
            "projects": await crud_project.get_all_projects(session),
        },
    )
