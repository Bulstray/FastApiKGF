from fastapi import APIRouter, Depends

from typing import Annotated

from core.schemas import ProgramRead

from sqlalchemy.orm import Session

from core.models import db_helper

router = APIRouter(tags=["Programs"])


@router.get("", response_model=list[ProgramRead])
def get_programs(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
):
    programs = db_helper.get_programs(session=session)
    return programs
