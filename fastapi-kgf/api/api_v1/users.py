from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

from core.models import User
from core.schemas import UserCreate, UserRead
from dependencies.providers import get_user_service
from services.user.service import UserService

router = APIRouter(tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserRead],
)
def get_all_users(
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> list[User]:
    """Endpoint for getting all users"""
    return user_service.get_all_users()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
def create_user(
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    user_create: UserCreate,
) -> User | None:
    """Endpoint for creating a new user"""
    return user_service.create_user(
        user_data=user_create,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    username: Annotated[str, Form()],
) -> None:
    """Endpoint for deleting a user"""
    return user_service.delete_user(
        username=username,
    )
