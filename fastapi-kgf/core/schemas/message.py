from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    task_id: int
    text: str
    author: int
    created_at: str

    model_config = ConfigDict(extra="ignore")
