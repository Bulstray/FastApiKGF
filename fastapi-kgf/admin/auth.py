from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from core.config.settings import SESSION_COOKIE_NAME
from core.types import UserRole
from dependencies.session_auth import get_authenticated_user


class AdminAuth(AuthenticationBackend):

    @staticmethod
    async def is_admin(
        request: Request,
        session_id: str | None = None,
    ) -> bool:
        if session_id is None:
            session_id = request.cookies.get(SESSION_COOKIE_NAME)
        user = await get_authenticated_user(request, session_id)
        return bool(user and user.role == UserRole.admin)

    async def authenticate(self, request: Request) -> bool:
        """Этот метод вызывается для каждого запроса к админке"""
        return await self.is_admin(request)
