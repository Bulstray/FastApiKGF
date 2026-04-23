from pydantic import BaseModel


class MessageReadStatusBase(BaseModel):
    """The base class for message status"""
    task_id: int
    users_id: list[int]
    count: int | None = None


class MessageReadStatus(MessageReadStatusBase):
    """The model for building the message status"""
