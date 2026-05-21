from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
    )

    tender_notification: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
    )
    task_notification: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
    )
    message_notification: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="settings",
    )
