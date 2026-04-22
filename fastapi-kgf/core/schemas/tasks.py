from datetime import date

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    """The base class for task"""
    title: str
    description: str
    deadline: date
    customer_id: int
    project_id: int


class TaskRead(TaskBase):
    filename: str | None = None
    folder_file: str | None = None

    model_config = ConfigDict(extra="ignore")


class TaskCreate(TaskBase):
    """Модель для создания задания"""
    rar_file: UploadFile

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
    )
