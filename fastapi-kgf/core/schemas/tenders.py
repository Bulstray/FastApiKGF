from pydantic import BaseModel, ConfigDict
from datetime import datetime


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
