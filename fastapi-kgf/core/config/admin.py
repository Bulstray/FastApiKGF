from pydantic import BaseModel

from core.enums import UserRole


class AdminConfig(BaseModel):
    username: str
    password: str
    role: UserRole
