from pathlib import Path

from aiopath import AsyncPath
from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import DatabaseConfig
from .platforms import PlatformConfig
from .redis_db import RedisConfig
from .session import SessionConfig
from .superuser import AdminSecretKey, SuperUserConfig
from .taskiq_config import TaskiqConfig

from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SESSION_COOKIE_NAME = "web_app_session_id"


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    programs: str = "/programs"
    users: str = "/users"
    login: str = "/login"
    logout: str = "/logout"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()


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
    taskiq: TaskiqConfig = TaskiqConfig()
    superuser: SuperUserConfig
    secret_key_admin: AdminSecretKey
    email_password: str

    uploads_program_dir: AsyncPath = AsyncPath("uploads/programs")
    uploads_file_task_dir: AsyncPath = AsyncPath("uploads/file_tasks")
    uploads_file_in_chat: AsyncPath = AsyncPath("uploads/file_in_chat")


settings = Settings()  # type: ignore[call-arg]
