from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime,
    Boolean, Enum, ForeignKey, BigInteger, Table
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')  # Создание бд

async_session = async_sessionmaker(engine)  # Подключение к бд

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
    Column('subscriber_id', Integer, ForeignKey('telegram_subscribers.id', ondelete='CASCADE'), primary_key=True),
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
    subscribers = relationship("TelegramSubscriber", secondary=organization_subscriptions,
                               back_populates="subscriptions")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    organizations = relationship("Organization", secondary=organization_writers, back_populates="writers")
    publications = relationship("Publication", back_populates="writer")


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())

    publications = relationship("Publication", secondary=publication_tags, back_populates="tags")


class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    featured_image_url = Column(String(255))
    writer_id = Column(Integer, ForeignKey('users.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    publish_date = Column(DateTime, nullable=False)
    event_start_date = Column(DateTime)
    event_end_date = Column(DateTime)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    writer = relationship("User", back_populates="publications")
    organization = relationship("Organization", back_populates="publications")
    tags = relationship("Tag", secondary=publication_tags, back_populates="publications")


class TelegramSubscriber(Base):
    __tablename__ = 'telegram_subscribers'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(100))
    subscribed_at = Column(DateTime, default=func.now())

    subscriptions = relationship("Organization", secondary=organization_subscriptions, back_populates="subscribers")


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
