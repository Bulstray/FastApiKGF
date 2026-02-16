from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services.files.programs import ProgramService
from services.users.service import UserService
from services.files.tasks_files.service import TasksFilesService
from core.config import settings


def get_program_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> ProgramService:
    return ProgramService(
        session=session,
        uploads_path=settings.uploads_program_dir,
    )


def get_tasks_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> TasksFilesService:
    return TasksFilesService(
        session=session,
        uploads_path=settings.uploads_file_task_dir,
    )


def get_user_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> UserService:
    return UserService(session=session)
