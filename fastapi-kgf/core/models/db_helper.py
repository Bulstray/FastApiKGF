from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str) -> None:
        self.engine = create_engine(
            url,
            echo=settings.db.echo,
        )

        self.session_factory = sessionmaker(bind=self.engine)

    def dispose(self) -> None:
        self.engine.dispose()

    def session_getter(self) -> Generator[Session]:
        with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=settings.db.url,
)
