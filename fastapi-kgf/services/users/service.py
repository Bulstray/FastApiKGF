from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from storage.db.base_crud import BaseCRUD


class UserService(BaseCRUD):
    """Service for users."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the service with a database connection and user class"""
        super().__init__(session, User)
