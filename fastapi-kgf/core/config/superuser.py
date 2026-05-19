from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr

from core.types import UserRole
from utils import hash_password

PasswordBytes = Annotated[
    str,
    AfterValidator(hash_password),
]


class SuperUserConfig(BaseModel):
    hashed_password: PasswordBytes
    name: str
    surname: str
    email: EmailStr
    role: UserRole = UserRole.admin


class AdminSecretKey(BaseModel):
    secret_key: str
