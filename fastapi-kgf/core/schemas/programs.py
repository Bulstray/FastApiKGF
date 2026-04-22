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

AuthorName = Annotated[
    str,
    Len(min_length=3, max_length=50),
]


class ProgramBase(BaseModel):
    """Base model for programs"""
    name: NameString
    description: DescriptionString
    author: AuthorName


class ProgramRead(ProgramBase):
    """A model for reading data about program"""

    file_size: str

    model_config = ConfigDict(from_attributes=True)


class ProgramCreate(ProgramBase):
    """A model for creating a program"""
