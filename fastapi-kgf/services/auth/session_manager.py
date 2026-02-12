import uuid
from time import time

from fastapi import Request

from core.config.settings import ACTIVE_SESSION, SESSION_COOKIE_NAME
from core.models import User
from core.schemas.user import UserRead


class SessionManager:
    @staticmethod
    def create_session(user: User):

        user_read = UserRead.model_validate(user)

        session_id = uuid.uuid4().hex

        ACTIVE_SESSION[session_id] = {**user_read.model_dump()}

        return session_id

    @staticmethod
    def delete_session(session_id: str, request: Request):
        ACTIVE_SESSION.pop(session_id, None)
        request.cookies.pop(SESSION_COOKIE_NAME)
