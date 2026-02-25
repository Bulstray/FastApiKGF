from pathlib import Path
from typing import Any

from aiopath import AsyncPath
from pydantic_settings import BaseSettings, SettingsConfigDict

from .api import ApiConfig
from .database import DatabaseConfig
from .platforms import PlatformConfig
from .redis_db import RedisConfig
from .session import SessionConfig
from .superuser import SuperUserConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SESSION_COOKIE_NAME = "web-app-session-id"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    api: ApiConfig = ApiConfig()
    tender_platform: PlatformConfig = PlatformConfig()
    session: SessionConfig = SessionConfig()
    superuser: SuperUserConfig

    uploads_program_dir: AsyncPath = AsyncPath("uploads/programs")
    uploads_file_task_dir: AsyncPath = AsyncPath("uploads/file_tasks")
    uploads_file_in_chat: AsyncPath = AsyncPath("uploads/file_in_chat")


settings = Settings()  # type: ignore[call-arg]
