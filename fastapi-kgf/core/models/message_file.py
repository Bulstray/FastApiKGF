from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .messages import Message


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
