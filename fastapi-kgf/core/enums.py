from enum import StrEnum


class UserRole(StrEnum):
    ADMIN: str = "admin"
    USER: str = "user"
    MODERATOR: str = "moderator"
