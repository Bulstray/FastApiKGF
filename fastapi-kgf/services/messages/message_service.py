from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MessageFile, Message
from services.files import FilesService
from storage.db import crud_message, crud_task_users
from core.schemas.message import Message as MessageSchema


class MessageManager:
    def __init__(
        self,
        session: AsyncSession,
        file_service: FilesService,
    ) -> None:
        self.session = session
        self.file_service = file_service

    async def get_messages_for_task(self, task_id: int) -> list[Message]:
        return await crud_message.get_messages_for_task(
            self.session,
            task_id,
        )

    async def add_message_in_db(
        self,
        message_data: dict[str, str],
    ) -> str | None:

        message_in = MessageSchema.model_validate(message_data)

        message_in_db = await crud_message.create_chats_message(
            session=self.session,
            message_in=message_in,
        )

        users_in_task = await crud_task_users.get_task_users(
            session=self.session,
            task_id=message_in.task_id,
        )

        for user_id in users_in_task:
            if message_in.author == user_id:
                continue

            await crud_message.update_count_unread(
                session=self.session,
                task_id=message_in.task_id,
                users_id=user_id,
            )

        if file_data := message_data.get("file"):

            file_path = await self.file_service.save_program_file_bs64(
                code_file=file_data.get("content"),
                filename=file_data.get("name"),
            )

            file = MessageFile(
                name=file_data.get("name"),
                folder_path=f"{file_path}",
                message_id=message_in_db,
            )

            file_folder = await crud_message.create_file_data_message(
                session=self.session,
                file=file,
            )

            return file_folder.folder_path

    async def get_unread_message(self, user_id: int) -> dict:
        return await crud_message.get_unread_message(
            session=self.session,
            user_id=user_id,
        )
