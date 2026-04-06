from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from dependencies.projects import get_project_service

from core.schemas.user import UserRead
from dependencies.session_auth import get_authenticated_user
from templating.jinja_template import templates

if TYPE_CHECKING:
    from services.projects.service import ProjectService
router = APIRouter()


@router.get("/", name="home")
async def home(
    request: Request,
    is_authenticated: Annotated[
        UserRead | None,
        Depends(get_authenticated_user),
    ],
    projects_service: Annotated[
        "ProjectService",
        Depends(get_project_service),
    ],
) -> HTMLResponse:
    projects = await projects_service.get_all_projects()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "is_authenticated": is_authenticated,
            "projects": projects,
        },
    )
