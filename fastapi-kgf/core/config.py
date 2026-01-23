from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_UPLOADS_PROGRAMS: Path = Path("uploads/programs")
BASE_UPLOADS_PROGRAMS.mkdir(parents=True, exist_ok=True)


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    programs: str = "/programs"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///database.db"
    echo: bool = False


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()
