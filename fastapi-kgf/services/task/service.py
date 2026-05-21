from aiopath import AsyncPath
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import FormData

from core.models import MessageReadStatus, Task, TaskUsers
from core.schemas import TaskCreate, TaskRead
from malling.send_email import send_email
from services.files import FilesService
from services.users.service import UserService
from storage.db.crud_tasks import TaskStorage


class TasksFilesService(TaskStorage):
    def __init__(
        self,
        session: AsyncSession,
        uploads_path: AsyncPath,
    ) -> None:
        super().__init__(session=session)
        self.file_service = FilesService(uploads_path=uploads_path)
        self.user_service = UserService(session=session)

    @staticmethod
    def get_executor_ids(form: FormData) -> list[int]:
        return [int(user_id) for user_id in form.getlist("executor_ids")]

    async def save_file_if_exists(
        self,
        task_model: TaskCreate,
        content: bytes,
    ) -> tuple[None, None] | tuple[str, str]:
        folder, filename = None, None

        if task_model.rar_file.filename:
            filename = task_model.rar_file.filename
            folder = await self.file_service.save_program_file(
                file=task_model.rar_file,
                content=content,
            )

        return folder, filename

    async def created_task(
        self,
        task_in: TaskRead,
        users_id: list[int],
    ) -> None:
        task = Task(**task_in.model_dump())

        task.task_users = [TaskUsers(user_id=user_id) for user_id in users_id]
        task.read_status = [
            MessageReadStatus(user_id=user_id) for user_id in users_id
        ]

        await self.create(task)

    async def create_task(
        self,
        form: FormData,
        content: bytes,
    ) -> None:

        task_create = TaskCreate.model_validate(form)

        folder, filename = await self.save_file_if_exists(
            task_create,
            content,
        )

        task_model = TaskRead(
            filename=filename,
            folder_file=f"{folder}",
            **task_create.model_dump(),
        )

        users_ids = self.get_executor_ids(form)

        # send message to email
        for user_id in users_ids:
            user = await self.user_service.get_by_id(user_id)
            if user.settings and user.settings.task_notification:
                await send_email(user.email, task_model)

        await self.created_task(
            task_in=task_model,
            users_id=[*users_ids, task_model.customer_id],
        )
