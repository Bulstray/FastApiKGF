from pydantic import BaseModel, ConfigDict


class MessageFile(BaseModel):
    name: str
    content: bytes


class MessageBase(BaseModel):
    """The basic model for messages"""

    task_id: int
    text: str
    author: int
    created_at: str
    file: MessageFile | None = None


class Message(MessageBase):
    """A model for storing messages"""

    model_config = ConfigDict(extra="ignore")
