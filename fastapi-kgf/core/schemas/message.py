from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    """The basic model for messages"""
    task_id: int
    text: str
    author: int
    created_at: str


class Message(MessageBase):
    """A model for storing messages"""
    model_config = ConfigDict(extra="ignore")
