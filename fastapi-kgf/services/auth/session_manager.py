import uuid

from core.models import User
from core.schemas.user import UserRead
from storage.redis import session


async def create_session(user: User) -> str:
    return await session.save_session(
        session_id=f"{uuid.uuid4().hex}",
        user=UserRead.model_validate(user),
    )


async def delete_session(session_id: str) -> None:
    await session.delete_by_session_id(
        session_id=session_id,
    )
