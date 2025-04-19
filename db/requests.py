# Здесь прописываем запросы к бд
from models import db, User, Organization, Tag, Publication, TelegramSubscriber, PublicationTag, OrganizationWriter, OrganizationSubscription
from sqlalchemy.exc import IntegrityError
from datetime import datetime


# -----------------------------
# USERS
# -----------------------------

def create_user(username, email, password_hash, role):
    user = User(username=username, email=email, password_hash=password_hash, role=role)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_all_users():
    return User.query.all()

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()


# -----------------------------
# ORGANIZATIONS
# -----------------------------

def create_organization(name, description=None, logo_url=None):
    org = Organization(name=name, description=description, logo_url=logo_url)
    db.session.add(org)
    db.session.commit()
    return org

def get_all_organizations():
    return Organization.query.all()

def get_organization_by_id(org_id):
    return Organization.query.get(org_id)


# -----------------------------
# TAGS
# -----------------------------

def create_tag(name):
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return tag

def get_all_tags():
    return Tag.query.all()

def get_tag_by_name(name):
    return Tag.query.filter_by(name=name).first()


# -----------------------------
# PUBLICATIONS
# -----------------------------

def create_publication(title, content, writer_id, organization_id, publish_date, featured_image_url=None, event_start_date=None, event_end_date=None, is_archived=False):
    pub = Publication(
        title=title,
        content=content,
        featured_image_url=featured_image_url,
        writer_id=writer_id,
        organization_id=organization_id,
        publish_date=publish_date,
        event_start_date=event_start_date,
        event_end_date=event_end_date,
        is_archived=is_archived
    )
    db.session.add(pub)
    db.session.commit()
    return pub

def get_publication_by_id(pub_id):
    return Publication.query.get(pub_id)

def get_all_publications():
    return Publication.query.all()

def get_publications_by_tag(tag_name):
    return Publication.query.join(PublicationTag).join(Tag).filter(Tag.name == tag_name).all()

def get_publications_by_writer(writer_id):
    return Publication.query.filter_by(writer_id=writer_id).all()

def get_publications_by_organization(organization_id):
    return Publication.query.filter_by(organization_id=organization_id).all()


# -----------------------------
# PUBLICATION-TAGS (связка)
# -----------------------------

def add_tag_to_publication(publication_id, tag_id):
    rel = PublicationTag(publication_id=publication_id, tag_id=tag_id)
    db.session.add(rel)
    db.session.commit()


# -----------------------------
# ORGANIZATION-WRITERS (связка)
# -----------------------------

def add_writer_to_organization(writer_id, organization_id):
    link = OrganizationWriter(writer_id=writer_id, organization_id=organization_id)
    db.session.add(link)
    db.session.commit()


# -----------------------------
# TELEGRAM SUBSCRIBERS
# -----------------------------

def create_telegram_subscriber(chat_id, username):
    sub = TelegramSubscriber(chat_id=chat_id, username=username)
    db.session.add(sub)
    db.session.commit()
    return sub

def get_subscriber_by_chat_id(chat_id):
    return TelegramSubscriber.query.filter_by(chat_id=chat_id).first()


# -----------------------------
# SUBSCRIPTIONS
# -----------------------------

def subscribe_to_organization(subscriber_id, organization_id):
    sub = OrganizationSubscription(subscriber_id=subscriber_id, organization_id=organization_id)
    db.session.add(sub)
    db.session.commit()

def get_organization_subscribers(organization_id):
    return TelegramSubscriber.query.join(OrganizationSubscription).filter(OrganizationSubscription.organization_id == organization_id).all()
