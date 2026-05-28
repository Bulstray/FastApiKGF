from pydantic_settings import BaseSettings
from .platforms import PlatformConfig
from .api import ApiPrefix
from .headers_requests import HEADERS


class Settings(BaseSettings):
    platforms: PlatformConfig = PlatformConfig()
    api: ApiPrefix = ApiPrefix()
    header_requests: dict[str, str] = HEADERS


settings = Settings()
