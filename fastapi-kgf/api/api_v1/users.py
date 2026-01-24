from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, status, Form
from sqlalchemy import Row
from sqlalchemy.orm import Session

from core.models import db_helper
from core.schemas import UserRead, UserCreate
from crud import user as crud_user

from core.models import User

router = APIRouter(tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserRead],
)
def get_users(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
) -> Sequence[Row[tuple[str, str]]] | None:

    return crud_user.get_all_users(
        session=session,
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
def create_user(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
    user_create: UserCreate,
) -> User:
    return crud_user.create_user(
        session=session,
        user_create=user_create,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
    username: str = Form(),
) -> None:
    return crud_user.delete_user(
        session=session,
        username=username,
    )
