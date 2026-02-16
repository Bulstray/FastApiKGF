from sqlalchemy.ext.asyncio import AsyncSession
from aiopath import AsyncPath
from services.files.files import FilesService
from fastapi import UploadFile

from core.schemas.tasks import TaskCreate
from core.models.task import Task

from storage.db import crud_tasks

from core.config import settings


class TasksFilesService:
    def __init__(
        self,
        session: AsyncSession,
        uploads_path: AsyncPath,
    ) -> None:
        self.session = session
        self.file_service = FilesService(uploads_path=uploads_path)

    async def get_tasks(self):
        result = await crud_tasks.get_all_tasks(session=self.session)
        return result

    async def get_task_by_title(self, title: str):
        result = await crud_tasks.get_task_by_title(
            session=self.session,
            title=title,
        )
        return result

    async def create_task(
        self, task: TaskCreate, file: UploadFile | None = None
    ) -> None:
        task_model = Task(**task.model_dump())
        await crud_tasks.create_file_in_db(
            session=self.session,
            task=task_model,
        )

        if file.filename:
            await self.file_service.save_program_file(file=file)

    async def delete_task(self, title):
        task = await self.get_task_by_title(title)

        if task.file:
            file_path = AsyncPath(rf"{settings.uploads_file_task_dir}\{task.file}")
            await self.file_service.delete_program_file(file=file_path)

        await crud_tasks.delete_tasks_in_db(
            session=self.session,
            title=title,
        )
