from pydantic import BaseModel
from uuid import UUID

class OrganizationBase(BaseModel):
    title: str
    description: str | None = None
    logo_path: str | None = None
    location: str | None = None
    contacts: str | None = None
    university_id: UUID

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationRead(OrganizationBase):
    id: UUID

    class Config:
        orm_mode = True
