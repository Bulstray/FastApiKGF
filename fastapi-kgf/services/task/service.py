from aiopath import AsyncPath
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import FormData

from core.models import Task
from core.schemas.message_read_status import MessageReadStatus
from core.schemas.tasks import Task as TaskSchema
from core.schemas.tasks import TaskCreate
from services.files import FilesService
from storage.db import crud_tasks, crud_user

from malling.send_email import send_email


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
    ) -> None:

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

        users_ids = [int(user_id) for user_id in form.getlist("executor_ids")] + [
            task_model.customer_id,
        ]

        # send message to email
        for user_id in users_ids[:-1]:
            user = await crud_user.get_user_by_id(self.session, user_id)
            await send_email(user.email, task_schema)

        await crud_tasks.add_task(
            session=self.session,
            task_in=task_model,
            user_ids=users_ids,
        )

    async def delete_task(self, id_task: id) -> Task:
        task = await self.get_task_by_id(id_task)

        await crud_tasks.delete_tasks_in_db(session=self.session, task=task)

        return task

    async def update_status_in_db(self, id_task: int) -> None:
        await crud_tasks.update_status_task(
            session=self.session,
            id_task=id_task,
        )

    async def get_tasks_by_project_id(
        self, project_id: int, user_id: int
    ) -> list[Task]:
        return await crud_tasks.get_tasks_by_project_id(
            self.session,
            project_id,
            user_id,
        )
