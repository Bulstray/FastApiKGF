import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from core.schemas.user import UserRead

from dependencies.session_auth import get_current_user
from templating.jinja_template import templates

from storage.db import crud_project, crud_keyword_tenders

from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

router = APIRouter()


@router.get("/", name="tenders:page")
async def tenders_page(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="tenders.html",
        context={
            "keywords": await crud_keyword_tenders.get_all_keywords_tender(
                session
            ),
            "user": current_user,
            "projects": await crud_project.get_all_projects(session),
            "today": datetime.datetime.now(),
        },
    )
