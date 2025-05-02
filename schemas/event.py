from pydantic import BaseModel
from uuid import UUID
from datetime import date, time
from decimal import Decimal

class EventBase(BaseModel):
    img_path: str | None = None
    title: str
    date_start: date
    date_end: date
    place: str
    time_start: time
    content: str
    priceint: Decimal
    action_title: str | None = None
    action_content: str | None = None
    organization_id: UUID
    relevance: bool = True

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: UUID

    class Config:
        orm_mode = True
