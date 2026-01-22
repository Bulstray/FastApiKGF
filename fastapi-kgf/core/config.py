from pydantic import AnyUrl, BaseModel
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///database.db"
    echo: bool = False
    autocommit: bool = False


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()