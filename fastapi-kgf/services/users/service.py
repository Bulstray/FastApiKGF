from sqlalchemy.ext.asyncio import AsyncSession

from storage.db.crud_user import UserStorage

from core.schemas import UserUpdateForm, UserUpdate


class UserService(UserStorage):
    """Service for users."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the service with a database connection and user class"""
        super().__init__(session)

    async def update_user_data(self, user_in: UserUpdateForm, user_id: int):
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
