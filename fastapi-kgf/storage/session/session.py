from core.config import settings

from redis import Redis
from core.schemas.user import UserRead

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.database.sessions,
    decode_responses=True,
)


class SessionStorage:

    @staticmethod
    def save_session(session_id: str, user: UserRead):
        redis.hset(
            name=settings.redis.collections_name.sessions_hash,
            key=session_id,
            value=user.model_dump_json(),
        )

    @staticmethod
    def delete_by_session_id(session_id: str):
        redis.hdel(
            settings.redis.collections_name.sessions_hash,
            session_id,
        )

    @staticmethod
    def get_by_session_id(session_id: str) -> UserRead | None:
        answer = redis.hget(
            name=settings.redis.collections_name.sessions_hash,
            key=session_id,
        )

        if answer:
            return UserRead.model_validate_json(answer)
        return None
