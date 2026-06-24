import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.models import Base, User, db_helper
from parsers.core import parse_tenders
from services.users.service import UserService
from storage.db.crud_user import get_user_by_email, create_user


async def scheduler():
    while True:
        await parse_tenders()
        # Ждем 24 часа (86400 секунд)
        await asyncio.sleep(86400)  # 24 * 60 * 60


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with db_helper.session_factory() as session:
        check_user = await get_user_by_email(
            session,
            settings.superuser.email,
        )

        if check_user is None:
            await create_user(session, settings.superuser)
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
