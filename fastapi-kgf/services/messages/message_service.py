from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MessageFile, Message
from services.files import FilesService
from storage.db import crud_message, crud_task_users
from core.schemas.message import Message as MessageSchema
from services.service_base import BaseService


class MessageManager(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        file_service: FilesService,
    ) -> None:
        super().__init__(session, Message)
        self.file_service = file_service

    async def get_messages_for_task(self, task_id: int) -> list[Message]:
        """
        Получить все сообщения для указанной задачи.

        Args:
            task_id: ID задачи

        Returns:
            Список сообщений для задачи
        """
        return await crud_message.get_messages_for_task(
            self.session,
            task_id,
        )

    async def set_unread_count_message(self, task_id: int, author_id: int) -> None:
        users_in_task = await crud_task_users.get_task_users(
            self.session,
            task_id,
        )

        for user_id in users_in_task:
            if author_id == user_id:
                continue
            await crud_message.update_mark_read_message(
                session=self.session,
                task_id=task_id,
                user_id=user_id,
            )

    async def process_message(
        self,
        message_in: MessageSchema,
    ) -> str | None:
        """
        Создать сообщение с опциональным файлом и обновить счётчики непрочитанных сообщений.

        Args:
            message_in: Данные сообщения, включая опциональные данные файла

        Returns:
            Словарь с ID сообщения и путём к файлу (если файл был загружен)
        """

        file_path = None

        message = Message(
            **message_in.model_dump(
                exclude={"file"},
            )
        )

        if message_in.file:
            file_path = await self.file_service.save_program_file_bs64(
                code_file=message_in.file.content,
                filename=message_in.file.name,
            )
            file = MessageFile(name=message_in.file.name, folder_path=f"{file_path}")

            message.file = file

        await self.create(message)

        await self.set_unread_count_message(
            task_id=message_in.task_id,
            author_id=message_in.author_id,
        )

        if file_path:
            return str(file_path)

    async def get_unread_message(self, user_id: int) -> dict:
        return await crud_message.get_unread_message(
            session=self.session,
            user_id=user_id,
        )
