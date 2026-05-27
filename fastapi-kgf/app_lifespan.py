import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core import broker
from core.config import settings
from core.models import Base, User, db_helper
from parsers.core import parse_tenders
from services.users.service import UserService


async def scheduler() -> None:
    while True:
        await parse_tenders()
        # Ждем 24 часа (86400 секунд)
        await asyncio.sleep(86400)  # 24 * 60 * 60


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    if not broker.is_worker_process:
        await broker.startup()

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with db_helper.session_factory() as session:

        user_service = UserService(session)

        check_user = await user_service.get_user_by_email(
            email=settings.superuser.email,
        )

        if check_user is None:
            admin = User(**settings.superuser.model_dump())
            await user_service.create(admin)

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
