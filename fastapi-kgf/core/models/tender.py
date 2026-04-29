from .base import Base

from sqlalchemy.orm import Mapped


class Tender(Base):
    __tablename__ = 'tenders'

    title: Mapped[str]
    organizer: Mapped[str]
    pub_date: Mapped[str]
