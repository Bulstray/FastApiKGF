from sqladmin.authentication import AuthenticationBackend
from starlette.responses import Response

from dependencies.session_auth import get_authenticated_user
from core.types import UserRole
from fastapi import Request


class AdminAuth(AuthenticationBackend):

    async def authenticate(self, request: Request) -> bool:
        return True
        """Этот метод вызывается для каждого запроса к админке"""
        user = await get_authenticated_user(request=request)
        if user and user.role == UserRole.admin:
            return True
        return False
