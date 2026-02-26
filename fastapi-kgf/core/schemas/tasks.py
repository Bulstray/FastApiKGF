from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    title: str
    description: str
    deadline: str
    executor_id: int
    customer_id: int
    filename: str | None = None
    folder_file: str | None = None

    model_config = ConfigDict(extra="ignore")


class TaskCreate(BaseModel):
    """Модель для создания задания"""

    title: str
    description: str
    deadline: str
    executor_id: int
    customer_id: int
    rar_file: UploadFile
