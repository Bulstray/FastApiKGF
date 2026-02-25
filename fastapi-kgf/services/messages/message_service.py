import base64

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Message, MessageFile
from storage.db import crud_message


class MessageManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message_in_db(self, message_data: dict[str, str], task_id: int):

        message = Message(
            initials="".join(
                [words[0] for words in message_data.get("author", "No Name").split()],
            ),
            task_id=task_id,
            text=message_data.get("text"),
            author=message_data.get("author"),
            created_at=message_data.get("time"),
        )

        message_in_db = await crud_message.create_chats_message(
            session=self.session,
            message=message,
        )

        if "file" in message_data:
            file_data = message_data.get("file")
            content = file_data.get("content").split(";base64,")[-1]

            with open(
                f'{settings.uploads_file_in_chat}/{file_data.get("name")}',
                "wb",
            ) as file_ctx:
                file_ctx.write(base64.b64decode(content))

            file = MessageFile(
                name=file_data.get("name"),
                folder_path=f'{settings.uploads_file_in_chat}/{file_data.get("name")}',
                message_id=message_in_db.id,
            )

            await crud_message.create_file_data_message(
                session=self.session,
                file=file,
            )
