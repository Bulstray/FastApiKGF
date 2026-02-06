from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services.programs import ProgramFilesService, ProgramService


def get_program_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    file_service: Annotated[
        ProgramFilesService,
        Depends(ProgramFilesService),
    ],
) -> ProgramService:
    return ProgramService(session=session, file_service=file_service)
