from typing import Annotated

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from core.models import Program, db_helper
from core.schemas import ProgramRead
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
) -> list[Program]:
    return list(crud_programs.get_all_programs(session=session))
