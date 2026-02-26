from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .message import Message


class MessageFile(Base):
    __tablename__ = "messages_files"

    message_id: Mapped[int] = mapped_column(
        ForeignKey(
            "messages.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    folder_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    message: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="file",
    )


@event.listens_for(MessageFile, "after_delete")
def delete_file_after_delete(mapper, connection, target):
    folder_path = Path(target.folder_path)
    if folder_path.exists():
        folder_path.unlink()
