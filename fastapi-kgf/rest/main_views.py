from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from starlette import status

from core.models import db_helper
from crud import programs as crud_programs
from crud.program_exceptions import ProgramNameDoesNotExistError
from dependencies.auth import validate_basic_auth
from templating.jinja_template import templates

router = APIRouter(include_in_schema=False)


@router.get("/", name="home")
def home_page(
    request: Request,
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
) -> HTMLResponse:
    context: dict[str, Any] = {}
    programs = crud_programs.get_all_programs(
        session=session,
    )

    context.update(
        programs=programs,
    )

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )


@router.get(
    "/program/{name}/",
    name="program:get",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(validate_basic_auth)],
)
def get_program(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
    name: str,
) -> FileResponse:
    result = crud_programs.get_file_by_name(
        session=session,
        name=name,
    )

    if result is None:
        raise ProgramNameDoesNotExistError(name)

    folder_path_str = result[0]
    folder_path = Path(folder_path_str)

    return FileResponse(
        filename=folder_path.name,
        path=str(folder_path),
    )
