from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.schemas import ProgramRead
from core.schemas.user import UserRead
from dependencies.providers import get_program_service
from dependencies.session_auth import get_current_user
from services.programs import ProgramService
from templating.jinja_template import templates
from services.projects.service import ProjectService
from dependencies.projects import get_project_service

router = APIRouter()


@router.get("/", name="programs:page")
async def programs_page(
    request: Request,
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
    ],
    is_authenticated: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    projects_service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
) -> HTMLResponse:
    """Render programs listing page."""

    programs = await program_service.get_all_programs()
    projects = await projects_service.get_all()

    programs_schemas = [
        ProgramRead.model_validate(
            program,
        )
        for program in programs
    ]

    return templates.TemplateResponse(
        request=request,
        name="programs.html",
        context={
            "programs": programs_schemas,
            "is_authenticated": is_authenticated,
            "projects": projects,
        },
    )
