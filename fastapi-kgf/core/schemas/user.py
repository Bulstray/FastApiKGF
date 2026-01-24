from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from core.enums import UserRole


def to_lowercase(value: str) -> str:
    return value.lower()


class UserBase(BaseModel):
    username: str
    password: str
    role: Annotated[
        UserRole,
        BeforeValidator(to_lowercase),
    ]


class User(UserBase):
    """Модель для хранения данных о пользователей"""


class UserCreate(UserBase):
    """Модель для создания данных о пользователей"""


class UserRead(BaseModel):
    username: str
    role: str
