from typing import Annotated

from pydantic import AfterValidator, BaseModel

from core.types import UserRole
from utils import hash_password

PasswordBytes = Annotated[str, AfterValidator(hash_password)]


class SuperUserConfig(BaseModel):
    username: str
    hashed_password: PasswordBytes
    role: UserRole = UserRole.admin
