from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .admin import AdminConfig
from .api import ApiConfig
from .database import DatabaseConfig
from .platforms import PlatformConfig

BASE_DIR = Path(__file__).resolve().parent.parent


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

    tender_platform: PlatformConfig = PlatformConfig()

    uploads_program_dir: Path = Path("uploads/programs")


settings = Settings()  # type: ignore[call-arg]
