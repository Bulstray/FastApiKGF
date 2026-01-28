from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.models import Base, db_helper
from core.schemas.user import UserCreate
from crud.user import create_user


def create_initial_admin() -> None:
    session_gen = db_helper.session_getter()
    session = next(session_gen)

    user_admin = UserCreate(
        username=settings.admin.username,
        password=settings.admin.password,
        role=settings.admin.role,
    )
    create_user(session=session, user_in=user_admin)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    Base.metadata.create_all(bind=db_helper.engine)

    create_initial_admin()

    yield None

    db_helper.dispose()
