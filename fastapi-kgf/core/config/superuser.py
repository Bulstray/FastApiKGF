from pydantic import BaseModel, EmailStr


class SuperUserConfig(BaseModel):
    email: EmailStr
    password: str
    is_active: bool = True
    is_superuser: bool = True
    is_verified: bool = True
