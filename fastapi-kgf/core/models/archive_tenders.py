from .base import Base
from sqlalchemy.orm import Mapped

from datetime import datetime


class ArchiveTender(Base):
    __tablename__ = "archive_tenders"

    name: Mapped[str]
    pub_date: Mapped[str]
    price: Mapped[str]
    organizer: Mapped[str]
    url: Mapped[str]
    end_date: Mapped[datetime]
    keyword_id: Mapped[int]
