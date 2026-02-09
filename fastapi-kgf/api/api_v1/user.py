from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

from core.models.user import User
from core.schemas.user import UserCreate, UserRead
from dependencies.providers import get_user_service
from services.users.service import UserService

router = APIRouter(tags=["Users"])


@router.get(
    "/",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> list[User]:
    return await user_service.get_all_users()


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> User | None:
    return await user_service.create_user(user)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    username: Annotated[str, Form(...)],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> None:
    return await user_service.delete_user(
        username=username,
    )
