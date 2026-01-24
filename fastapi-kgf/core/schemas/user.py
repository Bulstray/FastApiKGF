from utils import hash_password_simple
from pydantic import BaseModel, BeforeValidator, validator

from typing import Annotated

from core.enums import UserRole


def to_lowercase(value: str) -> str:
    return value.lower()


class UserBase(BaseModel):
    username: str
    password: Annotated[
        str,
        BeforeValidator(hash_password_simple),
    ]
    role: Annotated[
        UserRole,
        BeforeValidator(to_lowercase),
    ]
