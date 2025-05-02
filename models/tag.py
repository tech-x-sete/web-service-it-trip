from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class Tag(Base):
    __tablename__ = "tag"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)

    events = relationship("TagEvent", backref="tag", cascade="all, delete-orphan")
