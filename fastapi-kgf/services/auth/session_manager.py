import uuid

from core.models import User
from core.schemas.user import UserRead

from storage.session.session import SessionStorage


class SessionManager:
    @staticmethod
    def create_session(user: User):

        session_id = uuid.uuid4()

        SessionStorage.save_session(
            session_id=f"{session_id}",
            user=UserRead.model_validate(user),
        )

        return session_id

    @staticmethod
    def delete_session(session_id: str):

        SessionStorage.delete_by_session_id(
            session_id=session_id,
        )
