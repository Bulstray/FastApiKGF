from sqlalchemy.orm import Mapped

from .base import Base


class Program(Base):
    name: Mapped[str]
    description: Mapped[str]
    folder_path: Mapped[str]
    file_size: Mapped[str]
