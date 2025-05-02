from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base  # Убедитесь, что Base импортируется из правильного места
import uuid

class Organization(Base):
    __tablename__ = "organization"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # <- Это обязательно!
    title = Column(Text)
    description = Column(Text)
    logo_path = Column(Text)
    location = Column(Text)
    contacts = Column(Text)
    university_id = Column(UUID, ForeignKey("university.id"))

    users = relationship("UserOrganization", backref="organization", cascade="all, delete-orphan")
