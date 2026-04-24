from pydantic import BaseModel
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


class RedisConnectionConfig(BaseModel):
    host: str = REDIS_HOST
    port: int = REDIS_PORT


class RedisDatabaseConfig(BaseModel):
    default: int = 0
    sessions: int = 1
    tenders: int = 2
    chat_message: int = 3


class RedisCollectionConfig(BaseModel):
    sessions_hash: str = "sessions"
    tenders_hash: str = "tenders"


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    database: RedisDatabaseConfig = RedisDatabaseConfig()
    collections_name: RedisCollectionConfig = RedisCollectionConfig()
    decode_response: bool = True
