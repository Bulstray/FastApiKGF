from .base import Base

from sqlalchemy.orm import Mapped


class Task(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    description: Mapped[str]
    deadline: Mapped[str]
    executor: Mapped[str]
    customer: Mapped[str]
    file: Mapped[str | None]
