from pydantic import BaseModel


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
