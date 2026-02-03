from pathlib import Path

from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from .enums import UserRole

BASE_DIR = Path(__file__).resolve().parent.parent


class TenderPlatformConfig(BaseModel):
    etp_gpb: HttpUrl = (
        "https://new.etpgpb.ru/procedures.rss?page=1&per=100&procedure%5Bstage%5D%5B0%5D=accepting&sort=by_relevance&search="
    )

    tek_torg: HttpUrl = "https://www.tektorg.ru/procedures?name="


class AdminConfig(BaseModel):
    username: str
    password: str
    role: UserRole


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    programs: str = "/programs"
    users: str = "/users"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()


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
    admin: AdminConfig
    db: DatabaseConfig = DatabaseConfig()
    api: ApiConfig = ApiConfig()

    tender_platform: TenderPlatformConfig = TenderPlatformConfig()

    uploads_program_dir: Path = Path("uploads/programs")


settings = Settings()  # type: ignore
