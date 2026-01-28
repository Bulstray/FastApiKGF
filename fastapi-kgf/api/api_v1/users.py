from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from sqlalchemy import Row
from sqlalchemy.orm import Session

from core.models import User, db_helper
from core.schemas import UserCreate, UserRead
from crud import user as crud_user

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
) -> User | None:
    return crud_user.create_user(session=session, user_in=user_create)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
    username: Annotated[str, Form()],
) -> None:
    return crud_user.delete_user(
        session=session,
        username=username,
    )
