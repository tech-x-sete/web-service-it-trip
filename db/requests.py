from models import db_session, User, Organization, Tag, Publication, TelegramSubscriber
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# -----------------------------
# USERS
# -----------------------------

def create_user(username, email, password_hash, role):
    try:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        db_session.add(user)
        db_session.commit()
        return user
    except IntegrityError:
        db_session.rollback()
        return None

def get_user_by_id(user_id):
    return db_session.query(User).get(user_id)

def get_user_by_username(username):
    return db_session.query(User).filter_by(username=username).first()

def get_all_users():
    return db_session.query(User).all()

def update_user(user_id, **kwargs):
    user = get_user_by_id(user_id)
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        db_session.commit()
        return user
    return None

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db_session.delete(user)
        db_session.commit()

# -----------------------------
# ORGANIZATIONS
# -----------------------------

def create_organization(name, description=None, logo_url=None):
    try:
        org = Organization(
            name=name,
            description=description,
            logo_url=logo_url
        )
        db_session.add(org)
        db_session.commit()
        return org
    except IntegrityError:
        db_session.rollback()
        return None

def get_organization_by_id(org_id):
    return db_session.query(Organization).get(org_id)

def get_all_organizations():
    return db_session.query(Organization).all()

def update_organization(org_id, **kwargs):
    org = get_organization_by_id(org_id)
    if org:
        for key, value in kwargs.items():
            setattr(org, key, value)
        db_session.commit()
        return org
    return None

def delete_organization(org_id):
    org = get_organization_by_id(org_id)
    if org:
        db_session.delete(org)
        db_session.commit()

# -----------------------------
# TAGS
# -----------------------------

def create_tag(name):
    try:
        tag = Tag(name=name)
        db_session.add(tag)
        db_session.commit()
        return tag
    except IntegrityError:
        db_session.rollback()
        return None

def get_tag_by_id(tag_id):
    return db_session.query(Tag).get(tag_id)

def get_tag_by_name(name):
    return db_session.query(Tag).filter_by(name=name).first()

def get_all_tags():
    return db_session.query(Tag).all()

def delete_tag(tag_id):
    tag = get_tag_by_id(tag_id)
    if tag:
        db_session.delete(tag)
        db_session.commit()

# -----------------------------
# PUBLICATIONS
# -----------------------------

def create_publication(
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
                tag = get_tag_by_name(tag_name)
                if tag:
                    pub.tags.append(tag)
        
        db_session.add(pub)
        db_session.commit()
        return pub
    except IntegrityError:
        db_session.rollback()
        return None

def get_publication_by_id(pub_id):
    return db_session.query(Publication).get(pub_id)

def get_all_publications():
    return db_session.query(Publication).all()

def get_publications_by_organization(org_id):
    return db_session.query(Publication).filter_by(organization_id=org_id).all()

def get_publications_by_writer(writer_id):
    return db_session.query(Publication).filter_by(writer_id=writer_id).all()

def get_publications_by_tag(tag_name):
    tag = get_tag_by_name(tag_name)
    if tag:
        return tag.publications
    return []

def update_publication(pub_id, **kwargs):
    pub = get_publication_by_id(pub_id)
    if pub:
        for key, value in kwargs.items():
            setattr(pub, key, value)
        db_session.commit()
        return pub
    return None

def delete_publication(pub_id):
    pub = get_publication_by_id(pub_id)
    if pub:
        db_session.delete(pub)
        db_session.commit()

# -----------------------------
# ORGANIZATION-WRITERS (связка)
# -----------------------------

def add_writer_to_organization(writer_id, organization_id):
    writer = get_user_by_id(writer_id)
    org = get_organization_by_id(organization_id)
    if writer and org:
        org.writers.append(writer)
        db_session.commit()
        return True
    return False

def remove_writer_from_organization(writer_id, organization_id):
    writer = get_user_by_id(writer_id)
    org = get_organization_by_id(organization_id)
    if writer and org and writer in org.writers:
        org.writers.remove(writer)
        db_session.commit()
        return True
    return False

def get_organization_writers(org_id):
    org = get_organization_by_id(org_id)
    return org.writers if org else []

# -----------------------------
# PUBLICATION-TAGS (связка)
# -----------------------------

def add_tag_to_publication(publication_id, tag_id):
    pub = get_publication_by_id(publication_id)
    tag = get_tag_by_id(tag_id)
    if pub and tag:
        pub.tags.append(tag)
        db_session.commit()
        return True
    return False

def remove_tag_from_publication(publication_id, tag_id):
    pub = get_publication_by_id(publication_id)
    tag = get_tag_by_id(tag_id)
    if pub and tag and tag in pub.tags:
        pub.tags.remove(tag)
        db_session.commit()
        return True
    return False

# -----------------------------
# TELEGRAM SUBSCRIBERS
# -----------------------------

def create_telegram_subscriber(chat_id, username=None):
    try:
        sub = TelegramSubscriber(
            chat_id=chat_id,
            username=username
        )
        db_session.add(sub)
        db_session.commit()
        return sub
    except IntegrityError:
        db_session.rollback()
        return None

def get_subscriber_by_chat_id(chat_id):
    return db_session.query(TelegramSubscriber).filter_by(chat_id=chat_id).first()

def update_subscriber(chat_id, **kwargs):
    sub = get_subscriber_by_chat_id(chat_id)
    if sub:
        for key, value in kwargs.items():
            setattr(sub, key, value)
        db_session.commit()
        return sub
    return None

def delete_subscriber(chat_id):
    sub = get_subscriber_by_chat_id(chat_id)
    if sub:
        db_session.delete(sub)
        db_session.commit()

# -----------------------------
# ORGANIZATION SUBSCRIPTIONS
# -----------------------------

def subscribe_to_organization(chat_id, org_id):
    sub = get_subscriber_by_chat_id(chat_id)
    org = get_organization_by_id(org_id)
    if sub and org:
        org.subscribers.append(sub)
        db_session.commit()
        return True
    return False

def unsubscribe_from_organization(chat_id, org_id):
    sub = get_subscriber_by_chat_id(chat_id)
    org = get_organization_by_id(org_id)
    if sub and org and sub in org.subscribers:
        org.subscribers.remove(sub)
        db_session.commit()
        return True
    return False

def get_subscriber_organizations(chat_id):
    sub = get_subscriber_by_chat_id(chat_id)
    return sub.subscriptions if sub else []

def get_organization_subscribers(org_id):
    org = get_organization_by_id(org_id)
    return org.subscribers if org else []