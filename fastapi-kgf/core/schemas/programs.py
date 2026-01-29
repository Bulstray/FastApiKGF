from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, ConfigDict

DescriptionString = Annotated[
    str,
    MaxLen(max_length=500),
]

NameString = Annotated[
    str,
    Len(min_length=3, max_length=50),
]


class ProgramBase(BaseModel):
    name: NameString
    description: DescriptionString


class ProgramRead(ProgramBase):
    """Модель для чтения данных о программе"""

    file_size: str

    model_config = ConfigDict(from_attributes=True)


class ProgramCreate(ProgramBase):
    """Модель для создания данных о программе"""
