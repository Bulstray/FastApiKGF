from .base import Base

from sqlalchemy.orm import Mapped


class ParsingKeyword(Base):
    __tablename__ = 'parsing_keyword'

    decoding: Mapped[str]
    keyword: Mapped[str]
