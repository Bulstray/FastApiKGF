from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///database.db"
    echo: bool = False
