from .base import Base

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .parsing_keyword import ParsingKeyword


class Tender(Base):
    __tablename__ = "tenders"

    name: Mapped[str]
    pub_date: Mapped[str]
    price: Mapped[str]
    organizer: Mapped[str]
    url: Mapped[str]
    end_date: Mapped[datetime]
    keyword_id: Mapped[int] = mapped_column(
        ForeignKey(
            "parsing_keyword.id",
            ondelete="CASCADE",
        )
    )

    keyword: Mapped["ParsingKeyword"] = relationship(
        "ParsingKeyword",
        back_populates="tenders",
    )
