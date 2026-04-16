from pydantic import BaseModel


class CookiesBase(BaseModel):
    web_app_session_id: str | None = None


class Cookies(CookiesBase):
    """Model for cookies"""
