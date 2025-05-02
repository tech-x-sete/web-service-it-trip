from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str 

class UserRead(UserBase):
    id: UUID

    class Config:
        orm_mode = True
