from redis.asyncio import Redis

from core.config import settings
from core.schemas.user import UserRead

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.database.sessions,
    decode_responses=True,
)


class SessionStorage:

    @staticmethod
    async def save_session(session_id: str, user: UserRead) -> None:
        await redis.set(
            session_id,
            user.model_dump_json(),
            ex=48000,
        )

    @staticmethod
    async def delete_by_session_id(session_id: str) -> None:
        await redis.delete(session_id)

    @staticmethod
    async def get_by_session_id(session_id: str) -> UserRead | None:
        answer = await redis.get(session_id)

        if answer:
            return UserRead.model_validate_json(answer)
        return None
