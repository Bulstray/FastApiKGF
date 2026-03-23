from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str


class ProjectRead(BaseModel):
    """Модель для чтения проекта"""

    id: int

    class Config:
        from_attributes = True  # Вместо orm_mode


class ProjectCreate(ProjectBase):
    """Модель для создания проекта"""
