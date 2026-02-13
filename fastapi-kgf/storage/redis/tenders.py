from typing import cast

from redis import Redis

from core.config import settings

redis_tenders = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.database.tenders,
    decode_responses=True,
)


def save_tenders(key_word: str, tenders_str: str) -> None:
    redis_tenders.set(key_word, tenders_str, ex=3600)


def get_tenders(key_word: str) -> str | None:
    return cast("str | None", redis_tenders.get(key_word))
