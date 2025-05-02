from pydantic import BaseModel
from uuid import UUID

class TagEventBase(BaseModel):
    event_id: UUID
    tag_id: UUID

class TagEventCreate(TagEventBase):
    pass

class TagEventRead(TagEventBase):
    class Config:
        orm_mode = True
