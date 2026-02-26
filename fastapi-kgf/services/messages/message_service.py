from sqlalchemy.ext.asyncio import AsyncSession

from services.files import FilesService

from core.schemas.message import Message
from core.models import MessageFile
from storage.db import crud_message


class MessageManager:
    def __init__(self, session: AsyncSession, file_service: FilesService):
        self.session = session
        self.file_service = file_service

    async def add_message_in_db(self, message_data: dict[str, str]):

        message_in = Message.model_validate(message_data)

        message_in_db = await crud_message.create_chats_message(
            session=self.session,
            message_in=message_in,
        )

        if "file" in message_data:
            file_data = message_data.get("file")

            file_path = await self.file_service.save_program_file_bs64(
                code_file=file_data.get("content"),
                filename=file_data.get("name"),
            )

            file = MessageFile(
                name=file_data.get("name"),
                folder_path=f"{file_path}",
                message_id=message_in_db.id,
            )

            await crud_message.create_file_data_message(
                session=self.session,
                file=file,
            )
