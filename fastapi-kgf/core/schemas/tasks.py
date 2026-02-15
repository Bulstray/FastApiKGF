from pydantic import BaseModel

from datetime import datetime


class BaseTask(BaseModel):
    title: str
    description: str
    completed: datetime
    user_id: int
    created_at: int


class TaskRead(BaseTask):
    """Модель для чтения задач"""


class TaskCreate(BaseTask):
    """Модель для создания задач"""
