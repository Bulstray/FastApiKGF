import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from core.schemas.user import UserRead
from templating.jinja_template import templates
from services.tenders.key_word_service import KeyWordService
from dependencies.providers import get_keyword_tenders_service
from dependencies.projects import get_project_service
from dependencies.session_auth import get_current_user
from services.projects.service import ProjectService

router = APIRouter()


@router.get("/", name="tenders:page")
async def tenders_page(
    request: Request,
    keyword_service: Annotated[
        KeyWordService,
        Depends(get_keyword_tenders_service),
    ],
    current_user: Annotated[UserRead, Depends(get_current_user)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
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
            "today": datetime.datetime.today(),
        },
    )
