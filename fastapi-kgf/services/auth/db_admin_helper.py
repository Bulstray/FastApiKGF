from sqlalchemy.orm import Session

from core.config import settings
from services.auth.auth_helper import get_user_password, check_password_match


def validate_admin_password(
    session: Session,
    username: str,
    password: str,
) -> bool:

    db_password = get_user_password(
        username=username,
        session=session,
    )[0]

    if db_password is None:
        return False

    if db_password.role != settings.admin.role:
        return False

    return check_password_match(
        password1=db_password.password,
        password2=password,
    )
