from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .tenders import Tender


class ParsingKeyword(Base):
    __tablename__ = 'parsing_keyword'

    decoding: Mapped[str]
    keyword: Mapped[str]

    tenders: Mapped[list["Tender"]] = relationship(
        "Tender",
        back_populates="keyword",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
