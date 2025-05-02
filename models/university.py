from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import uuid

class University(Base):
    __tablename__ = "university"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    logo_path = Column(Text, nullable=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
