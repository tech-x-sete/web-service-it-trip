from core.domain import Publication, Tag
from infrastructure.db.models import async_session
from infrastructure.db.repositories.organization_repository import OrganizationRepository


async def publication_to_domain(pub) -> Publication:
    async with async_session() as session:
        repo = OrganizationRepository(session)
        organization = await repo.get_organization_by_id(pub.organization_id)
        return Publication(
            id=pub.id,
            title=pub.title,
            content=pub.content,
            featured_image_url=pub.featured_image_url,
            writer_id=pub.writer_id,
            organization=organization,
            publish_date=pub.publish_date,
            event_date=pub.event_date,
            is_archived=pub.is_archived,
            created_at=pub.created_at,
            location=pub.location,
        )


def tag_to_domain_simple(tag) -> Tag:
    return Tag(
        id=tag.id,
        name=tag.name,
        created_at=tag.created_at,
        # Не загружаем публикации, чтобы избежать рекурсии
        publications=[]
    )


def tag_to_domain(tag) -> Tag:
    return Tag(
        id=tag.id,
        name=tag.name,
        created_at=tag.created_at,
        publications=[publication_to_domain_simple(p) for p in tag.publications] if hasattr(tag, 'publications') else []
    )


def publication_to_domain_simple(pub) -> Publication:
    return pub(
        id=pub.id,
        title=pub.title,
        content=pub.content,
        featured_image_url=pub.featured_image_url,
        writer_id=pub.writer_id,
        organization_id=pub.organization_id,
        publish_date=pub.publish_date,
        event_start_date=pub.event_start_date,
        event_end_date=pub.event_end_date,
        is_archived=pub.is_archived,
        created_at=pub.created_at,
        updated_at=pub.updated_at,
        # Не загружаем теги, чтобы избежать рекурсии
        tags=[]
    )
