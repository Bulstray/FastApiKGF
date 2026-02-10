from fastapi import Cookie, Request

from core.config.settings import COOKIES, COOKIES_SESSION_ID_KEY


def is_authenticated(
    request: Request,
) -> bool:
    return request.cookies.get(COOKIES_SESSION_ID_KEY) in COOKIES
