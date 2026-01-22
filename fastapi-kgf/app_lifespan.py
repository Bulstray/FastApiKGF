from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from core.models import db_helper, Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await db_helper.dispose()
