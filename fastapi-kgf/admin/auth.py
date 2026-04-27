from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from core.config.settings import SESSION_COOKIE_NAME
from core.types import UserRole
from dependencies.session_auth import get_authenticated_user


class AdminAuth(AuthenticationBackend):

    async def authenticate(self, request: Request) -> bool:
        """Этот метод вызывается для каждого запроса к админке"""
        session_id = request.cookies.get(SESSION_COOKIE_NAME)
        user = await get_authenticated_user(request=request, session_id=session_id)
        if user and user.role == UserRole.admin:
            return True
        return False
