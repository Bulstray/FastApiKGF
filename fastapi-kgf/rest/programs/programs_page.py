from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies import ProjectFactory
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates
from dependencies.programs.programs import ProgramsFactory

router = APIRouter()


@router.get("/", name="programs:page")
async def programs_page(
    request: Request,
    program_service: Annotated[
        ProgramsFactory,
        Depends(ProgramsFactory),
    ],
    is_authenticated: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    projects_service: Annotated[
        ProjectFactory,
        Depends(ProjectFactory),
    ],
) -> HTMLResponse:
    """Render programs listing page."""

    programs = await program_service.get_all()
    projects = await projects_service.get_all()

    return templates.TemplateResponse(
        request=request,
        name="programs.html",
        context={
            "programs": programs,
            "is_authenticated": is_authenticated,
            "projects": projects,
        },
    )
