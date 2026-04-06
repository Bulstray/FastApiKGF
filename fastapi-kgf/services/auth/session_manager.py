import uuid

from core.models import User
from core.schemas.user import UserRead
from storage.redis import session


async def create_session(user: User) -> str:

    session_id = uuid.uuid4().hex

    await session.save_session(
        session_id=f"{session_id}",
        user=UserRead.model_validate(user),
    )

    return session_id


async def delete_session(session_id: str) -> None:

    await session.delete_by_session_id(
        session_id=session_id,
    )
