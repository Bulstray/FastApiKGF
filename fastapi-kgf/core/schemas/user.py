from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    field_validator,
)

from core.types import UserRole
from utils import hash_password

PasswordBytes = Annotated[str, AfterValidator(hash_password)]


class UserBase(BaseModel):
    """The base model user"""
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


class UserRead(UserBase):
    """Model for user read"""
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCreate(UserBase):
    """Model for user creation"""
