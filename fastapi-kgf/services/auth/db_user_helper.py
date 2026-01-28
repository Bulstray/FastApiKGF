from sqlalchemy.orm import Session

from services.auth.auth_helper import check_password_match, get_user_password


def validate_user_password(
    session: Session,
    username: str,
    password: str,
) -> bool:

    db_password = get_user_password(
        username=username,
        session=session,
    )

    if db_password is None:
        return False

    return check_password_match(
        password1=db_password[0].password,
        password2=password,
    )
