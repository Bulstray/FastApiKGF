from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.models import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    with db_helper.engine.begin() as connection:
        connection.run_sync(Base.metadata.create_all)  # type: ignore

    yield None

    db_helper.dispose()
