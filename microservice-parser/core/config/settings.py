from pydantic_settings import BaseSettings
from .platforms import PlatformConfig


class Settings(BaseSettings):
    platforms: PlatformConfig = PlatformConfig()
