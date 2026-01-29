from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Program(Base):
    __tablename__ = "programs"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    folder_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[str] = mapped_column(nullable=False)
