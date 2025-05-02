from sqlalchemy import Column, Text, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID 
from .base import Base
import uuid

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text)
    email = Column(Text)
    password = Column(Text)
    role = Column(Text)
    organizations = relationship("UserOrganization", backref="user", cascade="all, delete-orphan")
