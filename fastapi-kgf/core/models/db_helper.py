from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(
            url,
            echo=settings.db.echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=settings.db.url,
)
