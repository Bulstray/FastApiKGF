from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from core.models import db_helper
from services.programs import ProgramFilesService, ProgramService
from services.user.service import UserService


def get_program_service(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
    file_service: Annotated[
        ProgramFilesService,
        Depends(ProgramFilesService),
    ],
) -> ProgramService:
    return ProgramService(session=session, file_service=file_service)


def get_user_service(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
) -> UserService:
    return UserService(session=session)
