from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.models import Base, User, db_helper
from core.schemas import UserCreate

from api.dependencies.authentication.users import get_user_db
from api.dependencies.authentication.user_manager import get_user_manager
from api.dependencies.authentication.user_manager import UserManager

get_user_db_context = asynccontextmanager(get_user_db)
get_user_manager_context = asynccontextmanager(get_user_manager)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    user_create = UserCreate(
        email=settings.superuser.email,
        password=settings.superuser.password,
        is_active=settings.superuser.is_active,
        is_superuser=settings.superuser.is_superuser,
        is_verified=settings.superuser.is_verified,
    )

    async with db_helper.session_factory() as session:
        async with get_user_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                await user_manager.create(
                    user_create,
                    safe=False,
                )

    # Создаем папки
    await settings.uploads_program_dir.mkdir(exist_ok=True, parents=True)

    yield None

    await db_helper.dispose()
