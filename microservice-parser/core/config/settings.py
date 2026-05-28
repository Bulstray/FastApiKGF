from pydantic_settings import BaseSettings
from .platforms import PlatformConfig
from .api import ApiPrefix


class Settings(BaseSettings):
    platforms: PlatformConfig = PlatformConfig()
    api: ApiPrefix = ApiPrefix()
