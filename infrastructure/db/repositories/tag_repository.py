from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.ports.repositories import TagRepositoryPort
from core.domain.tag import Tag
from infrastructure.db.models import Tag as TagModel
from typing import Optional, List


class TagRepository(TagRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_tag(self, name: str) -> Optional[Tag]:
        try:
            tag = TagModel(name=name)
            self._session.add(tag)
            await self._session.commit()
            return self._to_domain(tag)
        except IntegrityError:
            await self._session.rollback()
            return None

    async def get_tag_by_id(self, tag_id: int) -> Optional[Tag]:
        tag = await self._session.get(TagModel, tag_id)
        return self._to_domain(tag) if tag else None

    async def get_tag_by_name(self, name: str) -> Optional[Tag]:
        result = await self._session.execute(
            select(TagModel).filter_by(name=name))
        tag = result.scalars().first()
        return self._to_domain(tag) if tag else None

    async def get_all_tags(self) -> List[Tag]:
        result = await self._session.execute(select(TagModel))
        return [self._to_domain(tag) for tag in result.scalars()]

    async def delete_tag(self, tag_id: int) -> bool:
        tag = await self._session.get(TagModel, tag_id)
        if not tag:
            return False

        await self._session.delete(tag)
        await self._session.commit()
        return True

    def _to_domain(self, tag) -> 'Tag':
        from infrastructure.converters import tag_to_domain
        return tag_to_domain(tag)

    # def _to_domain(self, tag: TagModel) -> Tag:
    #     return Tag(
    #         id=tag.id,
    #         name=tag.name,
    #         created_at=tag.created_at,
    #         publications=[self._publication_to_domain(p) for p in tag.publications] if tag.publications else []
    #     )

    # def _publication_to_domain(self, publication):
    #     from publication_repository import PublicationRepository
    #     return PublicationRepository._to_domain(None, publication)
    #
