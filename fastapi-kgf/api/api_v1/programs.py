from collections.abc import Sequence
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Form, UploadFile, status
from sqlalchemy import Row
from sqlalchemy.orm import Session

from core.models import db_helper
from core.schemas import ProgramCreate, ProgramRead
from crud import programs as crud_programs

router = APIRouter(tags=["Programs"])


@router.get(
    "",
    response_model=list[ProgramRead],
    status_code=status.HTTP_200_OK,
)
def get_programs(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
) -> Sequence[Row[tuple[Any, Any, Any]]]:
    return crud_programs.get_all_programs(session=session)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def add_program(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
    file: UploadFile,
    name: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
) -> None:
    program_create = ProgramCreate(
        name=name,
        description=description,
    )

    crud_programs.create_program(
        session=session,
        program_create=program_create,
        file=file,
    )


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_program(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    program_id: Annotated[int, Form(...)],
) -> None:
    crud_programs.delete_program(
        session=session,
        program_id=program_id,
    )
