from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .parsing_keyword import ParsingKeyword


class Tender(Base):
    __tablename__ = "tenders"

    name: Mapped[str]
    pub_date: Mapped[str]
    price: Mapped[str]
    organizer: Mapped[str]
    url: Mapped[str]
    end_date: Mapped[datetime] = mapped_column(nullable=True)
    keyword_id: Mapped[int] = mapped_column(
        ForeignKey(
            "parsing_keyword.id",
            ondelete="CASCADE",
        ),
    )

    keyword: Mapped["ParsingKeyword"] = relationship(
        "ParsingKeyword",
        back_populates="tenders",
    )
