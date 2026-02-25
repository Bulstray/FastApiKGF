from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    deadline: str
    executor_id: int
    customer_id: int
    file: str | None = None


class TaskCreate(TaskBase):
    """Модель для создания задания"""
