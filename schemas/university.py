from pydantic import BaseModel
from uuid import UUID

class UniversityBase(BaseModel):
    title: str
    description: str | None = None
    logo_path: str | None = None

class UniversityCreate(UniversityBase):
    pass

class UniversityRead(UniversityBase):
    id: UUID

    class Config:
        orm_mode = True
