from pydantic import BaseModel


class MessageReadStatus(BaseModel):
    task_id: int
    users_id: list[int]
    count: int | None = None
