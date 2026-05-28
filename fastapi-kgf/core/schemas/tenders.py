from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class BaseTender(BaseModel):
    """The base model for tenders"""

    name: str
    pub_date: str
    price: str
    organizer: str
    url: str
    keyword_id: int


class TenderCreate(BaseTender):
    """A model for create data storage"""

    model_config = ConfigDict(
        from_attributes=True,
    )

    end_date: datetime

    @field_validator("end_date", mode="before")
    @classmethod
    def parse_end_date(cls, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value
        # Парсим ваш формат "2026-05-29 09:00:00"
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
