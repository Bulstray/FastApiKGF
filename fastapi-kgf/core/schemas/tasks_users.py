from pydantic import BaseModel, ConfigDict


class TaskUsersBase(BaseModel):
    task_id: int
    executor_ids: list[int]

    model_config = ConfigDict(
        extra="ignore",
    )


class TaskUsersCreate(TaskUsersBase):
    """Модель для создания исполнителей для задачи"""
