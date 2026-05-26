import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies import KeyWordFactory, ProjectFactory
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates

router = APIRouter()


@router.get("/", name="tenders:page")
async def tenders_page(
    request: Request,
    keyword_service: Annotated[
        KeyWordFactory,
        Depends(KeyWordFactory),
    ],
    current_user: Annotated[UserRead, Depends(get_current_user)],
    project_service: Annotated[ProjectFactory, Depends(ProjectFactory)],
) -> HTMLResponse:
    key_words = await keyword_service.get_all()
    projects = await project_service.get_all()

    return templates.TemplateResponse(
        request=request,
        name="tenders.html",
        context={
            "keywords": key_words,
            "user": current_user,
            "projects": projects,
            "today": datetime.datetime.now(tz=datetime.UTC),
        },
    )
