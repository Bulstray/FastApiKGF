from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///database.db"
    echo: bool = False


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()
