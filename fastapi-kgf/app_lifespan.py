import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from core import broker
from core.config import settings
from core.models import Base, db_helper

from storage.db import crud_user
from tenders import parse_tenders


async def scheduler() -> None:
    while True:
        try:
            await parse_tenders()
        except Exception as e:
            print(e)
        # Ждем 12 часов
        await asyncio.sleep(43200)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if not broker.is_worker_process:
        await broker.startup()

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with db_helper.session_factory() as session:

        check_user = await crud_user.get_user_by_email(
            session=session,
            email=settings.superuser.email,
        )

        if check_user is None:
            await crud_user.create_user(
                session,
                settings.superuser,
            )

        await session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))

    # Создаем папки
    await settings.uploads_program_dir.mkdir(exist_ok=True, parents=True)
    await settings.uploads_file_task_dir.mkdir(exist_ok=True, parents=True)
    await settings.uploads_file_in_chat.mkdir(exist_ok=True, parents=True)

    background_tasks = set()
    task = asyncio.create_task(scheduler())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    app.state.scheduler_task = task

    yield None

    await db_helper.dispose()

    if not broker.is_worker_process:
        await broker.shutdown()
