from aiopath import AsyncPath
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas.tasks import Task as TaskSchema
from core.schemas.tasks_users import TaskUsersCreate as TaskUsersCreateSchema
from core.schemas.tasks import TaskCreate
from services.files import FilesService
from storage.db import crud_tasks
from storage.db import crud_task_users

from starlette.datastructures import FormData


class TasksFilesService:
    def __init__(
        self,
        session: AsyncSession,
        uploads_path: AsyncPath,
    ) -> None:
        self.session = session
        self.file_service = FilesService(uploads_path=uploads_path)

    async def get_tasks(self) -> list[Task]:
        return await crud_tasks.get_all_tasks(
            session=self.session,
        )

    async def get_task_by_id(self, task_id: int) -> Task | None:
        return await crud_tasks.get_task_by_id(
            session=self.session,
            task_id=task_id,
        )

    async def create_task(
        self,
        form: FormData,
        content: bytes,
    ) -> Task:

        folder = None
        filename = None

        task_schema = TaskCreate.model_validate(form)

        if task_schema.rar_file.filename:
            filename = task_schema.rar_file.filename
            folder = await self.file_service.save_program_file(
                file=task_schema.rar_file,
                content=content,
            )

        task_model = TaskSchema(
            filename=filename,
            folder_file=f"{folder}",
            **task_schema.model_dump(),
        )

        task_id = await crud_tasks.create_file_in_db(
            session=self.session,
            task_in=task_model,
        )

        task_users = TaskUsersCreateSchema(
            task_id=task_id,
            executor_ids=[int(user_id) for user_id in form.getlist("executor_ids")],
        )

        await crud_task_users.create_task_users(
            session=self.session,
            task_users=task_users,
        )

    async def delete_task(self, id_task: id) -> None:
        task = await self.get_task_by_id(id_task)

        await crud_tasks.delete_tasks_in_db(session=self.session, task=task)

    async def update_status_in_db(self, id_task: str, status: str) -> None:
        await crud_tasks.update_status_task(
            session=self.session,
            id_task=id_task,
            status=status,
        )
