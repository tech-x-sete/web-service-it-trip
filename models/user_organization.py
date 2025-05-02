from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class UserOrganization(Base):
    __tablename__ = "user_organization"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), primary_key=True)

