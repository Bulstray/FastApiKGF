from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.models import Base, User, db_helper
from crud import user as user_crud
from utils.password_service import hash_password


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаем папки
    await settings.uploads_program_dir.mkdir(exist_ok=True, parents=True)

    yield None

    await db_helper.dispose()
