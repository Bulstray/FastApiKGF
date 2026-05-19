from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    model_validator,
    ValidationError,
)

from core.types import UserRole
from utils import hash_password

PasswordBytes = Annotated[str, AfterValidator(hash_password)]


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None
    hashed_password: PasswordBytes | None = None


class UserUpdateForm(BaseModel):
    email: EmailStr
    new_password: str | None
    confirm_password: str | None

    @model_validator(mode="after")
    def check_password_match(self) -> "UserUpdateForm":
        if self.new_password != self.confirm_password:
            raise ValidationError("Passwords do not match")

        if not self.new_password:
            self.new_password = self.confirm_password = None

        return self


class UserBase(BaseModel):
    """The base model user"""

    hashed_password: PasswordBytes
    role: UserRole = UserRole.user
    name: str
    surname: str
    email: EmailStr


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
