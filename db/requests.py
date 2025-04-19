from models import db_session, User, Organization, Tag, Publication, TelegramSubscriber
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime


# -----------------------------
# USERS
# -----------------------------

async def create_user(username, email, password_hash, role):
    async with db_session() as session:
        try:
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role
            )
            session.add(user)
            await session.commit()
            return user
        except IntegrityError:
            await session.rollback()
            return None


async def get_user_by_id(user_id):
    async with db_session() as session:
        return await session.get(User, user_id)


async def get_user_by_username(username):
    async with db_session() as session:
        return (await session.execute(
            select(User).filter_by(username=username)
        )).scalars().first()


async def get_all_users():
    async with db_session() as session:
        return (await session.execute(
            select(User)
        )).scalars().all()


async def update_user(user_id, **kwargs):
    async with db_session() as session:
        user = await session.get(User, user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await session.commit()
            return user
        return None


async def delete_user(user_id):
    async with db_session() as session:
        user = await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()


# -----------------------------
# ORGANIZATIONS
# -----------------------------

async def create_organization(name, description=None, logo_url=None):
    async with db_session() as session:
        try:
            org = Organization(
                name=name,
                description=description,
                logo_url=logo_url
            )
            session.add(org)
            await session.commit()
            return org
        except IntegrityError:
            await session.rollback()
            return None


async def get_organization_by_id(org_id):
    async with db_session() as session:
        return await session.get(Organization, org_id)


async def get_all_organizations():
    async with db_session() as session:
        return (await session.execute(
            select(Organization)
        )).scalars().all()


async def update_organization(org_id, **kwargs):
    async with db_session() as session:
        org = await session.get(Organization, org_id)
        if org:
            for key, value in kwargs.items():
                setattr(org, key, value)
            await session.commit()
            return org
        return None


async def delete_organization(org_id):
    async with db_session() as session:
        org = await session.get(Organization, org_id)
        if org:
            await session.delete(org)
            await session.commit()


# -----------------------------
# TAGS
# -----------------------------

async def create_tag(name):
    async with db_session() as session:
        try:
            tag = Tag(name=name)
            session.add(tag)
            await session.commit()
            return tag
        except IntegrityError:
            await session.rollback()
            return None


async def get_tag_by_id(tag_id):
    async with db_session() as session:
        return await session.get(Tag, tag_id)


async def get_tag_by_name(name):
    async with db_session() as session:
        return (await session.execute(
            select(Tag).filter_by(name=name)
        )).scalars().first()


async def get_all_tags():
    async with db_session() as session:
        return (await session.execute(
            select(Tag)
        )).scalars().all()


async def delete_tag(tag_id):
    async with db_session() as session:
        tag = await session.get(Tag, tag_id)
        if tag:
            await session.delete(tag)
            await session.commit()


# -----------------------------
# PUBLICATIONS
# -----------------------------

async def create_publication(
        title,
        content,
        writer_id,
        organization_id,
        publish_date,
        featured_image_url=None,
        event_start_date=None,
        event_end_date=None,
        is_archived=False,
        tags=None
):
    async with db_session() as session:
        try:
            pub = Publication(
                title=title,
                content=content,
                writer_id=writer_id,
                organization_id=organization_id,
                publish_date=publish_date,
                featured_image_url=featured_image_url,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                is_archived=is_archived
            )

            if tags:
                for tag_name in tags:
                    tag = (await session.execute(
                        select(Tag).filter_by(name=tag_name)
                    )).scalars().first()
                    if tag:
                        pub.tags.append(tag)

            session.add(pub)
            await session.commit()
            return pub
        except IntegrityError:
            await session.rollback()
            return None


async def get_publication_by_id(pub_id):
    async with db_session() as session:
        return await session.get(Publication, pub_id)


async def get_all_publications():
    async with db_session() as session:
        return (await session.execute(
            select(Publication)
        )).scalars().all()


async def get_publications_by_organization(org_id):
    async with db_session() as session:
        return (await session.execute(
            select(Publication).filter_by(organization_id=org_id)
        )).scalars().all()


async def get_publications_by_writer(writer_id):
    async with db_session() as session:
        return (await session.execute(
            select(Publication).filter_by(writer_id=writer_id)
        )).scalars().all()


async def get_publications_by_tag(tag_name):
    async with db_session() as session:
        tag = (await session.execute(
            select(Tag).filter_by(name=tag_name)
        )).scalars().first()
        return tag.publications if tag else []


async def update_publication(pub_id, **kwargs):
    async with db_session() as session:
        pub = await session.get(Publication, pub_id)
        if pub:
            for key, value in kwargs.items():
                setattr(pub, key, value)
            await session.commit()
            return pub
        return None


async def delete_publication(pub_id):
    async with db_session() as session:
        pub = await session.get(Publication, pub_id)
        if pub:
            await session.delete(pub)
            await session.commit()


# -----------------------------
# ORGANIZATION-WRITERS (связка)
# -----------------------------

async def add_writer_to_organization(writer_id, organization_id):
    async with db_session() as session:
        writer = await session.get(User, writer_id)
        org = await session.get(Organization, organization_id)
        if writer and org:
            org.writers.append(writer)
            await session.commit()
            return True
        return False


async def remove_writer_from_organization(writer_id, organization_id):
    async with db_session() as session:
        writer = await session.get(User, writer_id)
        org = await session.get(Organization, organization_id)
        if writer and org and writer in org.writers:
            org.writers.remove(writer)
            await session.commit()
            return True
        return False


async def get_organization_writers(org_id):
    async with db_session() as session:
        org = await session.get(Organization, org_id)
        return org.writers if org else []


# -----------------------------
# PUBLICATION-TAGS (связка)
# -----------------------------

async def add_tag_to_publication(publication_id, tag_id):
    async with db_session() as session:
        pub = await session.get(Publication, publication_id)
        tag = await session.get(Tag, tag_id)
        if pub and tag:
            pub.tags.append(tag)
            await session.commit()
            return True
        return False


async def remove_tag_from_publication(publication_id, tag_id):
    async with db_session() as session:
        pub = await session.get(Publication, publication_id)
        tag = await session.get(Tag, tag_id)
        if pub and tag and tag in pub.tags:
            pub.tags.remove(tag)
            await session.commit()
            return True
        return False


# -----------------------------
# TELEGRAM SUBSCRIBERS
# -----------------------------

async def create_telegram_subscriber(chat_id, username=None):
    async with db_session() as session:
        try:
            sub = TelegramSubscriber(
                chat_id=chat_id,
                username=username
            )
            session.add(sub)
            await session.commit()
            return sub
        except IntegrityError:
            await session.rollback()
            return None


async def get_subscriber_by_chat_id(chat_id):
    async with db_session() as session:
        return (await session.execute(
            select(TelegramSubscriber).filter_by(chat_id=chat_id)
        )).scalars().first()


async def update_subscriber(chat_id, **kwargs):
    async with db_session() as session:
        sub = (await session.execute(
            select(TelegramSubscriber).filter_by(chat_id=chat_id)
        )).scalars().first()
        if sub:
            for key, value in kwargs.items():
                setattr(sub, key, value)
            await session.commit()
            return sub
        return None


async def delete_subscriber(chat_id):
    async with db_session() as session:
        sub = (await session.execute(
            select(TelegramSubscriber).filter_by(chat_id=chat_id)
        )).scalars().first()
        if sub:
            await session.delete(sub)
            await session.commit()


# -----------------------------
# ORGANIZATION SUBSCRIPTIONS
# -----------------------------

async def subscribe_to_organization(chat_id, org_id):
    async with db_session() as session:
        sub = (await session.execute(
            select(TelegramSubscriber).filter_by(chat_id=chat_id)
        )).scalars().first()
        org = await session.get(Organization, org_id)
        if sub and org:
            org.subscribers.append(sub)
            await session.commit()
            return True
        return False


async def unsubscribe_from_organization(chat_id, org_id):
    async with db_session() as session:
        sub = (await session.execute(
            select(TelegramSubscriber).filter_by(chat_id=chat_id)
        )).scalars().first()
        org = await session.get(Organization, org_id)
        if sub and org and sub in org.subscribers:
            org.subscribers.remove(sub)
            await session.commit()
            return True
        return False


async def get_subscriber_organizations(chat_id):
    async with db_session() as session:
        sub = (await session.execute(
            select(TelegramSubscriber).filter_by(chat_id=chat_id)
        )).scalars().first()
        return sub.subscriptions if sub else []


async def get_organization_subscribers(org_id):
    async with db_session() as session:
        org = await session.get(Organization, org_id)
        return org.subscribers if org else []
