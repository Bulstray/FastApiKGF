from sqlalchemy import String, Text
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
