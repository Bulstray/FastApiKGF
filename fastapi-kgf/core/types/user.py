from enum import StrEnum

UserIdType = int


class UserRole(StrEnum):
    user = "Пользователь"
    admin = "Администратор"
