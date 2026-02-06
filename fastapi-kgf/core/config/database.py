from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    url: str = "sqlite+aiosqlite:///database.db"
    echo: bool = False
