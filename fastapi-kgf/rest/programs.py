from typing import Annotated

from aiopath import AsyncPath
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

from core.schemas import ProgramRead
from dependencies.providers import get_program_service
from dependencies.session_auth import get_authenticated_user, require_auth
from services.programs import ProgramService
from templating.jinja_template import templates

router = APIRouter(prefix="/programs")


@router.get("/", name="programs:page")
async def programs_page(
    request: Request,
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
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
        context={"programs": programs_schemas},
    )


@router.get(
    "/{name}/download",
    name="program:download",
    response_model=None,
)
async def download_program(
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
    ],
    user: Annotated[dict, Depends(require_auth)],
    name: str,
) -> RedirectResponse | FileResponse:

    program = await program_service.get_program_by_name(program_name=name)

    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program {name} not found",
        )

    file_path = AsyncPath(program.folder_path)

    if not await file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found in server",
        )

    return FileResponse(
        str(file_path),
        filename=file_path.name,
    )
