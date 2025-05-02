from pydantic import BaseModel
from uuid import UUID

class TagBase(BaseModel):
    title: str

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: UUID

    class Config:
        orm_mode = True
