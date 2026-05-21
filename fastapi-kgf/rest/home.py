from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies import ProjectFactory
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates

router = APIRouter()


@router.get("/", name="home")
async def home(
    request: Request,
    is_authenticated: Annotated[
        UserRead | None,
        Depends(get_current_user),
    ],
    projects_service: Annotated[
        ProjectFactory,
        Depends(ProjectFactory),
    ],
) -> HTMLResponse:
    projects = await projects_service.get_all()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "is_authenticated": is_authenticated,
            "projects": projects,
        },
    )
