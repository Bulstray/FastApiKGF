from pathlib import Path
from aiopath import AsyncPath

from pydantic_settings import BaseSettings, SettingsConfigDict

from .superuser import SuperUserConfig
from .api import ApiConfig
from .database import DatabaseConfig
from .platforms import PlatformConfig
from .access_token import AccessToken

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    superuser: SuperUserConfig
    db: DatabaseConfig = DatabaseConfig()
    api: ApiConfig = ApiConfig()

    tender_platform: PlatformConfig = PlatformConfig()
    access_token: AccessToken

    uploads_program_dir: AsyncPath = AsyncPath("uploads/programs")


settings = Settings()  # type: ignore[call-arg]
