from fastapi import HTTPException, status
from fastapi.security import HTTPBasic

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic username and password",
    auto_error=True,
)

admin_basic_auth = HTTPBasic(
    scheme_name="Admin Basic Auth",
    description="Basic authentication for administrators",
    auto_error=True,
)


def raise_auth_error() -> None:
    """Выбрасывает стандартную ошибку аунтефикации"""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
