from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    Boolean, Enum, ForeignKey, BigInteger, Table
)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum
from core import domain

from pathlib import Path
import os

from sqlalchemy.orm import selectinload

# # Для всех связей добавляем стратегии загрузки
# Publication.tags = relationship("Tag",
#                               secondary=publication_tags,
#                               back_populates="publications",
#                               lazy="selectin")

db_dir = Path(__file__).parent

# Подключение к базе данных в папке db
engine = create_async_engine(url=f'sqlite+aiosqlite:///{db_dir}/db.sqlite3')  # Создание бд

async_session = async_sessionmaker(engine, expire_on_commit=False)  # Подключение к бд

Base = declarative_base()


# ---------------------------
# ENUM для ролей
# ---------------------------

class RoleEnum(enum.Enum):
    moderator = "moderator"
    writer = "writer"
    guest = "guest"


# ---------------------------
# Вспомогательные таблицы
# ---------------------------

organization_writers = Table(
    'organization_writers',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=True),
    Column('writer_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, default=func.now())
)

publication_tags = Table(
    'publication_tags',
    Base.metadata,
    Column('publication_id', Integer, ForeignKey('publications.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

organization_subscriptions = Table(
    'organization_subscriptions',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=True),
    Column('subscribed_at', DateTime, default=func.now())
)


# ---------------------------
# Основные таблицы
# ---------------------------

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    logo_url = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    writers = relationship("User", secondary=organization_writers, back_populates="organizations")
    publications = relationship("Publication", back_populates="organization")

    @staticmethod
    def to_domain(self) -> domain.Organization:
        return domain.Organization(
            id=self.id,
            name=self.name,
            description=self.description,
            logo_url=self.logo_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
            writers=self.writers,
            publications=self.publications
        )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    login = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    organizations = relationship("Organization",
                                 secondary=organization_writers,
                                 back_populates="writers")
    publications = relationship("Publication", back_populates="writer")

    @staticmethod
    def to_domain(self) -> domain.User:
        return domain.User(
            id=self.id,
            username=self.username,
            login=self.login,
            password_hash=self.password_hash,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.udated_at,
            organizations=self.organizations,
            publications=self.publications
        )


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())

    publications = relationship("Publication", secondary=publication_tags, back_populates="tags")

    @staticmethod
    def to_domain(self) -> domain.Tag:
        return domain.Tag(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            publications=self.publications
        )


class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    featured_image_url = Column(String(255))
    writer_id = Column(Integer, ForeignKey('users.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    publish_date = Column(DateTime, nullable=False)
    event_date = Column(DateTime)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    location = Column(Text)

    writer = relationship("User", back_populates="publications")
    organization = relationship("Organization", back_populates="publications")
    tags = relationship("Tag", secondary=publication_tags, back_populates="publications")

    @staticmethod
    def to_domain(self) -> domain.Publication:
        return domain.Publication(
            id=self.id,
            title=self.title,
            content=self.content,
            featured_image_url=self.featured_image_url,
            writer_id=self.writer_id,
            organization=self.organization,
            publish_date=self.publish_date,
            event_date=self.event_date,
            is_archived=self.is_archived,
            created_at=self.created_at,
            location=self.location,
        )


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
