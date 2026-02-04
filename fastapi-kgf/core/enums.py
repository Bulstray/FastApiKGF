from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class Platform(StrEnum):
    gazp = "GAZP"
    rosh = "ROSH"
