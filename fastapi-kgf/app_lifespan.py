from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI
from sqlalchemy.orm import Session

from core.models import Base, db_helper
from core.config import settings
from core.schemas.user import UserCreate
from crud.user import create_user


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    create_user(
        session=db_helper.session_getter(),
        user_in=UserCreate(
            username=settings.admin.username,
            password=settings.admin.password,
            role=settings.admin.role,
        ),
    )

    Base.metadata.create_all(bind=db_helper.engine)

    yield None

    db_helper.dispose()
