from pathlib import Path

from sqlalchemy import String, Text, event
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Program(Base):
    __tablename__ = "programs"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    folder_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
    )

    file_size: Mapped[str] = mapped_column(
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )


@event.listens_for(Program, "after_delete")
def delete_file_after_delete(mapper, connection, target) -> None:
    folder_file = Path(target.folder_file)
    if folder_file.exists():
        folder_file.unlink()
