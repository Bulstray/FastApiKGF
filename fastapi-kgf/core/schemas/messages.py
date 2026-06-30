from pydantic import BaseModel

from pydantic import ConfigDict, model_validator

from core.models import Message

from utils.file_size import sync_get_file_size

from pathlib import Path


class MessageFile(BaseModel):
    name: str
    content: str


class MessageBase(BaseModel):
    """The basic model for messages"""

    task_id: int
    text: str
    author: int
    created_at: str
    file: MessageFile | None = None


class MessageCreate(MessageBase):
    """A model for storing messages"""

    model_config = ConfigDict(extra="ignore")


class MessageFileRead(BaseModel):
    name: str
    folder_path: str
    size: str


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    author: str
    created_at: str
    initials: str
    file: MessageFileRead | None = None

    @model_validator(mode='before')
    @classmethod
    def extract_from_sqlalchemy(cls, data: Message):
        message_data = {
            "id": data.id,
            "text": data.text,
            "author": data.user.full_name,
            "created_at": str(data.created_at),
            "initials": data.user.initials,
        }

        if data.file:

            size = sync_get_file_size(Path(data.file.folder_path))
            message_data.update(
                file={
                    "name": data.file.name,
                    "folder_path": data.file.folder_path,
                    "size": size,
                },
            )

        return message_data
