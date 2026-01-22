from pathlib import Path
from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel

NameString = Annotated[
    str,
    MaxLen(max_length=500),
]

DescriptionString = Annotated[
    str,
    Len(min_length=3, max_length=50),
]


class ProgramBase(BaseModel):
    name: NameString
    description: DescriptionString
    folder_path: Path


class Program(ProgramBase):
    """Модель для хранения данных о программе"""


class ProgramRead(ProgramBase):
    """Модель для чтения данных о программе"""


class ProgramCreate(ProgramBase):
    """Модель для создания данных о программе"""
