from enum import StrEnum

UserIdType = int


class UserRole(StrEnum):
    user = "user"
    admin = "admin"
