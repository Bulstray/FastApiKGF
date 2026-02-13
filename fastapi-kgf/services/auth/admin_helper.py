import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from core.types import UserRole
from storage.db.crud_user import get_user_by_username


class AdminHelper:
    @staticmethod
    async def check_password_match(
        hashed_password: bytes,
        password: bytes,
    ) -> bool:
        """Проверка пароля на совпадения"""
        return bcrypt.checkpw(
            hashed_password=hashed_password,
            password=password,
        )

    async def validate_admin_password(
        self,
        username: str,
        password: str,
        session: AsyncSession,
    ) -> bool:
        db_user = await get_user_by_username(
            session=session,
            username=username,
        )

        if db_user is None or db_user.role != UserRole.admin:
            return False

        return await self.check_password_match(
            hashed_password=db_user.hashed_password.encode("utf-8"),
            password=password.encode("utf-8"),
        )


admin_helper = AdminHelper()
