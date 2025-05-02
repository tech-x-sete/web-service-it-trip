from sqlalchemy import Column, Text, Date, Time, Boolean, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class Event(Base):
    __tablename__ = "event"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    img_path = Column(Text)
    title = Column(Text)
    date_start = Column(Date)
    date_end = Column(Date)
    place = Column(Text)
    time_start = Column(Time)
    content = Column(Text)
    priceint = Column(DECIMAL)
    action_title = Column(Text)
    action_content = Column(Text)
    relevance = Column(Boolean, default=True)

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"))

    organization = relationship("Organization", backref="events")
    tags = relationship("TagEvent", backref="event", cascade="all, delete-orphan")
