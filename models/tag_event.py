from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class TagEvent(Base):
    __tablename__ = "tag_event"

    event_id = Column(UUID(as_uuid=True), ForeignKey("event.id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tag.id"), primary_key=True)
