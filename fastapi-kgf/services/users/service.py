from sqlalchemy.ext.asyncio import AsyncSession

from storage.db.crud_user import UserStorage


class UserService(UserStorage):
    """Service for users."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the service with a database connection and user class"""
        super().__init__(session)
