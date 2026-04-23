from pydantic import BaseModel, ConfigDict


class TaskUsersBase(BaseModel):
    """The base class for the user's tasks"""
    task_id: int
    executor_ids: list[int]


class TaskUsersCreate(TaskUsersBase):
    """A model for creating a user task"""

    model_config = ConfigDict(
        extra="ignore",
    )
