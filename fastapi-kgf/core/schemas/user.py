from typing import Annotated

from pydantic import AfterValidator, BaseModel, field_validator, EmailStr, ConfigDict

from core.types import UserRole
from utils import hash_password

PasswordBytes = Annotated[str, AfterValidator(hash_password)]


class UserBase(BaseModel):
    username: str
    hashed_password: PasswordBytes
    role: UserRole = UserRole.user
    name: str
    surname: str
    email: EmailStr

    @field_validator("username")
    @classmethod
    def to_lower(cls, v: str) -> str:
        return v.lower()


class UserRead(BaseModel):
    username: str
    role: UserRole
    name: str
    surname: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCreate(UserBase):
    """Модель для создания пользователя"""
