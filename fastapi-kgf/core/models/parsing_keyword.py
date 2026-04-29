from sqlalchemy.orm import Mapped

from .base import Base


class ParsingKeyword(Base):
    __tablename__ = "parsing_keyword"

    decoding: Mapped[str]
    keyword: Mapped[str]
