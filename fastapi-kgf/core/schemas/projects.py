from pydantic import BaseModel


class ProjectBase(BaseModel):
    """Base model for project"""
    name: str


class ProjectRead(BaseModel):
    """A model for reading a project"""

    id: int

    class Config:
        from_attributes = True  # Вместо orm_mode


class ProjectCreate(ProjectBase):
    """A model for creating a project"""
