from core.config.settings import COOKIES_SESSION_ID_KEY

from fastapi import Request


def get_session(request: Request) -> bool:
    session = request.cookies.get(COOKIES_SESSION_ID_KEY)

    if session is None:
        return False

    return True
