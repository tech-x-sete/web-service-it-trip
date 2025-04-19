from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.ports.repositories import PublicationRepositoryPort
from core.domain.publication import Publication
from infrastructure.db.models import (
    Publication as PublicationModel,
    Tag as TagModel,
    User as UserModel,
    Organization as OrganizationModel, async_session
)
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import selectinload

from infrastructure.db.repositories.organization_repository import OrganizationRepository


class PublicationRepository(PublicationRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_publication(
            self,
            title: str,
            content: str,
            writer_id: int,
            organization_id: int,  # Возможно здесь что-то
            publish_date: datetime,
            featured_image_url: Optional[str] = None,
            event_start_date: Optional[datetime] = None,
            event_end_date: Optional[datetime] = None,
            is_archived: bool = False,
            tags: Optional[List[str]] = None
    ) -> Optional[Publication]:
        try:
            async with async_session() as session:
                repo = OrganizationRepository(session)
                organization = repo.get_organization_by_id(organization_id)

            pub = PublicationModel(
                title=title,
                content=content,
                writer_id=writer_id,
                organization=organization,
                publish_date=publish_date,
                featured_image_url=featured_image_url,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                is_archived=is_archived
            )

            if tags:
                for tag_name in tags:
                    result = await self._session.execute(
                        select(TagModel).filter_by(name=tag_name))
                    tag = result.scalars().first()
                    if tag:
                        pub.tags.append(tag)

            self._session.add(pub)
            await self._session.commit()
            return await self._to_domain(pub)
        except IntegrityError:
            await self._session.rollback()
            return None

    async def get_publication_by_id(self, pub_id: int) -> Optional[Publication]:
        pub = await self._session.get(PublicationModel, pub_id)
        return self._to_domain(pub) if pub else None

    async def get_all_publications(self) -> List[Publication]:
        result = await self._session.execute(
            select(PublicationModel).options(
                selectinload(PublicationModel.tags),
                selectinload(PublicationModel.writer),
                selectinload(PublicationModel.organization)
            )
        )
        pubs = result.scalars().all()
        return [await self._to_domain(pub) for pub in pubs]

    async def get_publications_by_organization(self, org_id: int) -> List[Publication]:
        result = await self._session.execute(
            select(PublicationModel).filter_by(organization_id=org_id))
        return [await self._to_domain(pub) for pub in result.scalars()]

    async def get_publications_by_writer(self, writer_id: int) -> List[Publication]:
        result = await self._session.execute(
            select(PublicationModel).filter_by(writer_id=writer_id))
        return [await self._to_domain(pub) for pub in result.scalars()]

    async def get_publications_by_tag(self, tag_name: str) -> List[Publication]:
        result = await self._session.execute(
            select(TagModel).filter_by(name=tag_name))
        tag = result.scalars().first()
        return [await self._to_domain(pub) for pub in tag.publications] if tag else []

    async def update_publication(self, pub_id: int, **kwargs: Any) -> Optional[Publication]:
        pub = await self._session.get(PublicationModel, pub_id)
        if not pub:
            return None

        for key, value in kwargs.items():
            setattr(pub, key, value)
        await self._session.commit()
        return await self._to_domain(pub)

    async def delete_publication(self, pub_id: int) -> bool:
        pub = await self._session.get(PublicationModel, pub_id)
        if not pub:
            return False

        await self._session.delete(pub)
        await self._session.commit()
        return True

    async def add_tag_to_publication(self, publication_id: int, tag_id: int) -> bool:
        pub = await self._session.get(PublicationModel, publication_id)
        tag = await self._session.get(TagModel, tag_id)

        if not pub or not tag:
            return False

        pub.tags.append(tag)
        await self._session.commit()
        return True

    async def remove_tag_from_publication(self, publication_id: int, tag_id: int) -> bool:
        pub = await self._session.get(PublicationModel, publication_id)
        tag = await self._session.get(TagModel, tag_id)

        if not pub or not tag or tag not in pub.tags:
            return False

        pub.tags.remove(tag)
        await self._session.commit()
        return True

    async def _to_domain(self, pub) -> 'Publication':
        from infrastructure.converters import publication_to_domain
        result = await publication_to_domain(pub)
        return result

    # def _to_domain(self, pub: PublicationModel) -> Publication:
    #     # from user_repository import UserRepository
    #     # from organization_repository import OrganizationRepository
    #     from .tag_repository import TagRepository
    #
    #     return Publication(
    #         id=pub.id,
    #         title=pub.title,
    #         content=pub.content,
    #         featured_image_url=pub.featured_image_url,
    #         writer_id=pub.writer_id,
    #         organization_id=pub.organization_id,
    #         publish_date=pub.publish_date,
    #         event_start_date=pub.event_start_date,
    #         event_end_date=pub.event_end_date,
    #         is_archived=pub.is_archived,
    #         created_at=pub.created_at,
    #         updated_at=pub.updated_at,
    #         tags=[TagRepository._to_domain(t) for t in pub.tags] if pub.tags else []
    #     )
