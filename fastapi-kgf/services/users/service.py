from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from core.schemas.user import UserCreate
from crud.user import create_user as crud_create_user
from crud.user import delete_user as crud_delete_user
from crud.user import get_all_users as crud_get_all_users
from crud.user import get_user_by_username as crud_get_user_by_username

from .exception import UserAlreadyExistsErorr

USER_ALREADY_EXISTS_ERROR_MSG = "User already exists"


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> list[User]:
        return await crud_get_all_users(session=self.session)

    async def get_user_by_name(self, username: str) -> User | None:
        return await crud_get_user_by_username(
            session=self.session,
            username=username.lower(),
        )

    async def create_user(self, user_in: UserCreate) -> User | None:
        user = User(**user_in.model_dump())

        if await self.get_user_by_name(username=user.username):
            raise UserAlreadyExistsErorr(USER_ALREADY_EXISTS_ERROR_MSG)

        return await crud_create_user(
            session=self.session,
            user=user,
        )

    async def delete_user(self, username: str) -> None:
        return await crud_delete_user(
            session=self.session,
            username=username.lower(),
        )
