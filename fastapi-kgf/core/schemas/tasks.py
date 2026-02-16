from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    deadline: str
    executor: str
    customer: str
    file: str | None = None


class TaskCreate(TaskBase):
    """Модель для создания задания"""
