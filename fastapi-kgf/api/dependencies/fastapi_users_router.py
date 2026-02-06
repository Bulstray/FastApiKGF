from fastapi_users import FastAPIUsers


from core.models import User
from core.types import UserIdType

from .user_manager import get_user_manager

from .backend import authentication_backend

fastapi_users_router = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)
