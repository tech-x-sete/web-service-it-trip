from pydantic import BaseModel
from uuid import UUID

class UserOrganizationBase(BaseModel):
    user_id: UUID
    organization_id: UUID

class UserOrganizationCreate(UserOrganizationBase):
    pass

class UserOrganizationRead(UserOrganizationBase):
    class Config:
        orm_mode = True
