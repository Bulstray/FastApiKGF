from fastapi import APIRouter, Depends, Request

from fastapi.responses import HTMLResponse
from typing import Annotated
from core.schemas import UserRead
from dependencies.session_auth import get_current_user
from dependencies.projects import get_project_service
from services.projects.service import ProjectService
from templating.jinja_template import templates

router = APIRouter(prefix="/profile")


@router.get("/", name="profile:page")
async def profile_page(
    request: Request,
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    project_service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
) -> HTMLResponse:
    projects = await project_service.get_all()

    return templates.TemplateResponse(
        "profile.html",
        context={
            "user": current_user,
            "projects": projects,
            "request": request,
        },
    )
