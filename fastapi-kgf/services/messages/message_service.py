import json

from aiopath import AsyncPath
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MessageFile, Message
from services.files import FilesService
from storage.db import crud_task_users
from core.schemas.message import Message as MessageSchema
from storage.db.crud_message import MessageStorage

from utils.file_size import get_file_size


class MessageManager(MessageStorage):
    """
    A manager for working with messages.

    Responsible for business logic related to messages,
    including integration with the file service
    for handling attachments.

    Attributes:
        session (AsyncSession): Asynchronous database session.
        file_service (FilesService): Service for working with files (attachments).
    """

    def __init__(
        self,
        session: AsyncSession,
        file_service: FilesService,
    ) -> None:
        """
        Initialize the message manager.

        Args:
            session (AsyncSession): Asynchronous SQLAlchemy session for database interaction.
            file_service (FilesService): Instance of the file service.
        """
        super().__init__(session)
        self.file_service = file_service

    async def set_unread_count_message(
        self,
        task_id: int,
        author_id: int,
    ) -> None:
        """
        Updates unread message counters for users in a task (excluding the author).

        For all users participating in the specified task, except the message author,
        marks new messages as unread. This ensures recipients see notifications
        about new messages.

        Args:
            task_id (int): The unique identifier of the task. Used to fetch
                the list of users participating in the task.
            author_id (int): The identifier of the user who sent the message.
                This user's unread counters are not updated (since they sent the message).

        Returns:
            None: This method performs updates in the database and does not return
                any value.
        """
        users_in_task = await crud_task_users.get_task_users(
            self.session,
            task_id,
        )

        for user_id in users_in_task:
            if author_id == user_id:
                continue
            await self.update_count_unread(
                task_id=task_id,
                user_id=user_id,
            )

    async def create_message_db(
        self,
        message_in: MessageSchema,
    ) -> AsyncPath | None:
        """
        Creates a new message in the database, optionally with an attached file.

        Processes an input message schema, saves any attached file to storage,
        and persists the message to the database. If a file is included,
        it's decoded and saved, and a reference is linked to the message.

        Args:
             message_in (MessageSchema): Input schema containing message data
                and optional file attachment. Must include all required message fields;
                file is optional.

        Returns:
            str | None: The filesystem path where the file was saved if a file
                was attached and successfully saved. Returns None if no file was
                included.
        """
        file_path = None

        message = Message(
            **message_in.model_dump(exclude={"file"}),
        )

        if message_in.file:
            file_path = await self.file_service.save_program_file_bs64(
                code_file=message_in.file.content,
                filename=message_in.file.name,
            )
            file = MessageFile(
                name=message_in.file.name,
                folder_path=f"{file_path}",
            )

            message.file = file

        await self.create(message)

        return file_path

    async def process_message(
        self,
        message_in: str,
    ) -> dict:
        """
        Создать сообщение с опциональным файлом и обновить счётчики непрочитанных сообщений.

        Args:
            message_in: Данные сообщения, включая опциональные данные файла

        Returns:
            Словарь с ID сообщения и путём к файлу (если файл был загружен)
        """

        message_schema = MessageSchema.model_validate(json.loads(message_in))

        file_path = await self.create_message_db(
            message_schema,
        )

        await self.set_unread_count_message(
            task_id=message_schema.task_id,
            author_id=message_schema.author,
        )

        message_data = message_schema.model_dump(
            exclude={"file"},
        )

        if file_path:
            message_data.update(
                file={
                    "name": message_schema.file.name,
                    "folder_path": str(file_path),
                    "size": await get_file_size(file_path),
                }
            )

        return message_data
