from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from services.task.service import TasksFilesService


class TaskFactory(TasksFilesService):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ):
        super().__init__(
            session,
            settings.uploads_file_task_dir,
        )
