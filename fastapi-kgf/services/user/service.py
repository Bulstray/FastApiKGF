from sqlalchemy.orm import Session

from core.models import User
from core.schemas import UserCreate
from crud.user import create_user as crud_create_user
from crud.user import delete_user as crud_delete_user
from crud.user import get_all_users as crud_get_all_users
from crud.user import get_user_by_username as crud_get_user_by_username
from crud.user_exceptions import UserAlreadyExistsError
from utils import hash_password


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_users(self) -> list[User]:
        """Получить всех пользователей"""
        return crud_get_all_users(self.session)

    def get_user_by_username(self, username: str) -> User | None:
        """Получить пользователей по username"""
        return crud_get_user_by_username(
            session=self.session,
            username=username,
        )

    def create_user(self, user_data: UserCreate) -> User:
        """Создание нового пользователя плюс валидацией"""
        existing_user = self.get_user_by_username(user_data.username)
        if existing_user:
            raise UserAlreadyExistsError(user_data.username)

        user = User(
            username=user_data.username,
            password=hash_password(user_data.password),
            role=user_data.role,
        )

        return crud_create_user(session=self.session, user=user)

    def delete_user(self, username: str) -> None:
        return crud_delete_user(
            session=self.session,
            username=username,
        )
