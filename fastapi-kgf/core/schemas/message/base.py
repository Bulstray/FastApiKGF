from pydantic import BaseModel

from .file import MessageFile


class MessageBase(BaseModel):
    """The basic model for messages"""

    task_id: int
    text: str
    author: int
    created_at: str
    file: MessageFile | None = None
