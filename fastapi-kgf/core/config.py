from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_UPLOADS_PROGRAMS: Path = Path("uploads/programs")
BASE_UPLOADS_PROGRAMS.mkdir(parents=True, exist_ok=True)


class Admin(BaseModel):
    username: str
    password: str
    role: str


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    programs: str = "/programs"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///database.db"
    echo: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DatabaseConfig = DatabaseConfig()
    api: ApiPrefix = ApiPrefix()
    admin: Admin


settings = Settings()
