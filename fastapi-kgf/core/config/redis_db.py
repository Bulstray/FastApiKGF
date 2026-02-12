from pydantic import BaseModel


class RedisConnectionConfig(BaseModel):
    host: str
    port: int


class RedisDatabaseConfig(BaseModel):
    default: int = 0
    sessions: int = 1


class RedisConfig(BaseModel):
    # connection: RedisConnectionConfig = RedisConnectionConfig()
    database: RedisDatabaseConfig = RedisDatabaseConfig()
