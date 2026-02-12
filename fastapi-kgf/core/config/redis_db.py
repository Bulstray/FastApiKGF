from pydantic import BaseModel


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6378


class RedisDatabaseConfig(BaseModel):
    default: int = 0
    sessions: int = 1


class RedisCollectionConfig(BaseModel):
    sessions_hash: str = "sessions"


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    database: RedisDatabaseConfig = RedisDatabaseConfig()
    collections_name: RedisCollectionConfig = RedisCollectionConfig()
