from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.ports.repositories import OrganizationRepositoryPort
from core.domain.organization import Organization
from core.domain.user import User
from infrastructure.db.models import (
    Organization as OrganizationModel,
    User as UserModel
)
from typing import Optional, List


class OrganizationRepository(OrganizationRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_organization(self, name: str, description: Optional[str] = None,
                                  logo_url: Optional[str] = None) -> Optional[Organization]:
        try:
            org = OrganizationModel(
                name=name,
                description=description,
                logo_url=logo_url
            )
            self._session.add(org)
            await self._session.commit()
            return self._to_domain(org)
        except IntegrityError:
            await self._session.rollback()
            return None

    async def get_organization_by_id(self, org_id: int) -> Optional[Organization]:
        org = await self._session.get(OrganizationModel, org_id)
        return self._to_domain(org) if org else None

    async def get_all_organizations(self) -> List[Organization]:
        result = await self._session.execute(select(OrganizationModel))
        return [self._to_domain(org) for org in result.scalars()]

    async def add_writer(self, writer_id: int, organization_id: int) -> bool:
        writer = await self._session.get(UserModel, writer_id)
        org = await self._session.get(OrganizationModel, organization_id)

        if not writer or not org:
            return False

        org.writers.append(writer)
        await self._session.commit()
        return True

    # Остальные методы реализуются аналогично

    def _to_domain(self, org: OrganizationModel) -> Organization:
        return Organization(
            id=org.id,
            name=org.name,
            description=org.description,
            logo_url=org.logo_url,
            created_at=org.created_at,
            updated_at=org.updated_at,
            writers=[self._user_to_domain(u) for u in org.writers] if org.writers else []
        )

    def _user_to_domain(self, user: UserModel) -> User:
        from user_repository import UserRepository
        return UserRepository._to_domain(None, user)  # Используем метод из UserRepository
