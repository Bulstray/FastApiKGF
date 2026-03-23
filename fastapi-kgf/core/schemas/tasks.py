from datetime import date

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    title: str
    description: str
    deadline: date
    customer_id: int
    filename: str | None = None
    folder_file: str | None = None
    project_id: int

    model_config = ConfigDict(extra="ignore")


class TaskCreate(BaseModel):
    """Модель для создания задания"""

    title: str
    description: str
    deadline: date
    customer_id: int
    rar_file: UploadFile
    project_id: int

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
    )
