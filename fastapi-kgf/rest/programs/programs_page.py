from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.schemas import ProgramRead
from core.schemas.user import UserRead
from dependencies.providers import get_program_service
from services.programs import ProgramService
from templating.jinja_template import templates
from dependencies.session_auth import require_auth

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
        Depends(require_auth),
    ],
) -> HTMLResponse:
    """Render programs listing page."""

    programs = await program_service.get_all_programs()

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
        },
    )
