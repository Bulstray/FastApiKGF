from aiopath import AsyncPath
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.tasks import TaskCreate
from core.schemas.tasks import Task as TaskSchema
from services.files import FilesService
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
        task_in: TaskCreate,
        content: bytes,
    ) -> None:

        folder = None
        filename = None

        if task_in.rar_file.filename:
            filename = task_in.rar_file.filename
            folder = await self.file_service.save_program_file(
                file=task_in.rar_file,
                content=content,
            )

        task = TaskSchema(
            filename=filename,
            folder_file=f"{folder}",
            **task_in.model_dump(),
        )
        await crud_tasks.create_file_in_db(session=self.session, task_in=task)

    async def delete_task(self, id_task: id):
        task = await self.get_task_by_id(id_task)

        await crud_tasks.delete_tasks_in_db(session=self.session, task=task)

    async def update_status_in_db(self, title: str, status: str):
        await crud_tasks.update_status_task(
            session=self.session,
            title=title,
            status=status,
        )
