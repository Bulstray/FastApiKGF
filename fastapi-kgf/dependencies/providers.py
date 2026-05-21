from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from services.programs import ProgramService


async def get_program_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> ProgramService:
    return ProgramService(
        session=session,
        uploads_path=settings.uploads_program_dir,
    )
