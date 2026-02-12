from pydantic import BaseModel


class SessionConfig(BaseModel):
    cookie_session_id: str = "web-app-session-id"
