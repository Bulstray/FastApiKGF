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


class UserLogin(BaseModel):
    username: str
    password: str


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

    @property
    def full_name(self) -> str:
        return f"{self.name.capitalize()} {self.surname.capitalize()}"

    @property
    def initials(self) -> str:
        return f"{self.name[0]}{self.surname[0]}".upper()

    model_config = ConfigDict(
        from_attributes=True,
    )
