from pydantic import BaseModel


class CookiesBase(BaseModel):
    """The basic model for cookies"""
    web_app_session_id: str | None = None


class Cookies(CookiesBase):
    """Model for cookies"""
