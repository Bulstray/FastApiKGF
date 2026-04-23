from aiopath import AsyncPath
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import FormData

from core.models import Task
from core.schemas import TaskRead
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

    async def create_task(
        self,
        form: FormData,
        content: bytes,
    ) -> None:

        folder, filename = None, None

        task_schema = TaskCreate.model_validate(form)

        if task_schema.rar_file.filename:
            filename = task_schema.rar_file.filename
            folder = await self.file_service.save_program_file(
                file=task_schema.rar_file,
                content=content,
            )

        task_model = TaskRead(
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

    async def get_tasks_by_project_id(
        self, project_id: int, user_id: int
    ) -> list[Task]:
        return await crud_tasks.get_tasks_by_project_id(
            self.session,
            project_id,
            user_id,
        )
