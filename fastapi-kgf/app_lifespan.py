from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.models import Base, User, db_helper
from storage.db import crud_user


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with db_helper.session_factory() as session:

        check_user = await crud_user.get_user_by_username(
            session=session,
            username=settings.superuser.username,
        )

        if check_user is None:
            admin = User(
                username=settings.superuser.username,
                hashed_password=settings.superuser.hashed_password,
                role=settings.superuser.role,
                name=settings.superuser.name,
                email=settings.superuser.email,
                surname=settings.superuser.surname,
            )
            await crud_user.create_user(
                session=session,
                user=admin,
            )

    # Создаем папки
    await settings.uploads_program_dir.mkdir(exist_ok=True, parents=True)

    yield None

    await db_helper.dispose()
