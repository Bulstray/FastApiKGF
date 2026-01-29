from sqlalchemy.orm import Session

from core.config import settings
from services.auth.auth_service import (
    authenticate_user,
)


def validate_admin(
    session: Session,
    username: str,
    password: str,
) -> bool:

    user = authenticate_user(
        session=session,
        username=username,
        password=password,
    )

    return bool(user and user.role == settings.admin.role)
