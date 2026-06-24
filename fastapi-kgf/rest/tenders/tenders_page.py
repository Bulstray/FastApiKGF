import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates

from core.models import db_helper
from storage.db.crud_project import get_all_projects
from storage.db.crud_keyword_tenders import get_all_keywords_tender

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
            "user": current_user,
            "today": datetime.datetime.today(),
            "projects": await get_all_projects(session),
            "keywords": await get_all_keywords_tender(session),
        },
    )
