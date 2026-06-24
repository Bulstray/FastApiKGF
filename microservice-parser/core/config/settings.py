from pydantic_settings import BaseSettings

from .api import ApiPrefix
from .headers_requests import HEADERS
from .platforms import PlatformConfig


class Settings(BaseSettings):
    platforms: PlatformConfig = PlatformConfig()
    api: ApiPrefix = ApiPrefix()
    header_requests: dict[str, str] = HEADERS


settings = Settings()
