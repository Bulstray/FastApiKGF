from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import FileResponse, HTMLResponse
from starlette import status

from core.schemas import ProgramRead
from dependencies.auth import validate_basic_auth
from dependencies.providers import get_program_service
from services.programs import ProgramService
from templating.jinja_template import templates

router = APIRouter(include_in_schema=False)


@router.get("/", name="home")
def home_page(
    request: Request,
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
    ],
) -> HTMLResponse:

    programs = program_service.get_all_programs()

    programs_schemas = [ProgramRead.model_validate(program) for program in programs]

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"programs": programs_schemas},
    )


@router.get(
    "/program/{name}/download",
    name="program:download",
    dependencies=[Depends(validate_basic_auth)],
)
def download_program(
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
    ],
    name: str,
) -> FileResponse:
    program = program_service.get_program_by_name(program_name=name)

    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program {name} not found",
        )

    file_path = Path(program.folder_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File not found in server",
        )

    return FileResponse(
        str(file_path),
        filename=file_path.name,
    )
