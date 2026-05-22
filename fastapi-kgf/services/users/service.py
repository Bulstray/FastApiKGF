import bcrypt
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import UserLogin, UserUpdate, UserUpdateForm
from services.auth.session_manager import create_session
from storage.db.crud_user import UserStorage


class UserService(UserStorage):
    """Service for users."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the service with a database connection and user class"""
        super().__init__(session)

    async def validate_basic_auth_user(self, request: Request) -> str | None:
        async with request.form() as user_data:
            user = UserLogin.model_validate(user_data)

        is_user = await self.get_user_by_email(user.email.lower())

        if is_user and bcrypt.checkpw(
            password=user.password.encode("utf-8"),
            hashed_password=is_user.hashed_password.encode("utf-8"),
        ):
            return await create_session(is_user)

        return None

    async def update_user_data(
        self, user_in: UserUpdateForm, user_id: int,
    ) -> None:
        user_data = UserUpdate(
            email=user_in.email,
            hashed_password=(
                user_in.new_password if user_in.new_password else None
            ),
        )

        user = await self.get_by_id(user_id)

        if user_in.email == user.email:
            user_in.email = None

        user_in_dump = user_data.model_dump(exclude_none=True)

        if user_in_dump:
            await self.update_data_user(user_in_dump, user_id)
