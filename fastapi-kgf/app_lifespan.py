from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.models import Base, User, db_helper
from crud import user as user_crud
from utils.password_service import hash_password


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=db_helper.engine)

    with db_helper.session_factory() as session:
        admin = user_crud.get_user_by_username(
            session=session,
            username=settings.admin.username,
        )

        if not admin:
            hashed_password = hash_password(settings.admin.password)

            admin_user = User(
                username=settings.admin.username,
                password=hashed_password,
                role=settings.admin.role,
            )

            session.add(admin_user)
            session.commit()

    # Создаем папки
    settings.uploads_program_dir.mkdir(exist_ok=True, parents=True)

    yield None

    db_helper.dispose()
