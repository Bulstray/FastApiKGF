from aiopath import AsyncPath
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.task import Task
from core.schemas.tasks import TaskCreate
from services.files.files import FilesService
from storage.db import crud_tasks


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

    async def get_task_by_id(self, task_id: int):
        result = await crud_tasks.get_task_by_id(
            session=self.session,
            task_id=task_id,
        )
        return result

    async def create_task(
        self,
        task: TaskCreate,
        file: UploadFile | None = None,
    ) -> None:
        task_model = Task(**task.model_dump())
        await crud_tasks.create_file_in_db(
            session=self.session,
            task=task_model,
        )

        if file.filename:
            file_name = await self.file_service.save_program_file(file=file)

    async def delete_task(self, id_task: id):
        task = await self.get_task_by_id(id_task)

        if task.file:
            file_path = AsyncPath(rf"{settings.uploads_file_task_dir}\{task.file}")
            await self.file_service.delete_program_file(file=file_path)

        for file_in_chat in task.messages:
            if file_in_chat.file:
                file = AsyncPath(file_in_chat.file.folder_path)
                await file.unlink()

        await crud_tasks.delete_tasks_in_db(session=self.session, task=task)

    async def update_status_in_db(self, title: str, status: str):
        await crud_tasks.update_status_task(
            session=self.session,
            title=title,
            status=status,
        )
