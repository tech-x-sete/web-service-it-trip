from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.ports.repositories import UserRepositoryPort
from core.domain.user import User, UserRole
from infrastructure.db.models import User as UserModel
from typing import Optional, List


class UserRepository(UserRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, username: str, email: str, password_hash: str, role: str) -> Optional[User]:
        try:
            user = UserModel(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role
            )
            self._session.add(user)
            await self._session.commit()
            return self._to_domain(user)
        except IntegrityError:
            await self._session.rollback()
            return None

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        user = await self._session.get(UserModel, user_id)
        return self._to_domain(user) if user else None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self._session.execute(
            select(UserModel).filter_by(username=username)
        )
        user = result.scalars().first()
        return self._to_domain(user) if user else None

    async def get_all_users(self) -> List[User]:
        result = await self._session.execute(select(UserModel))
        return [self._to_domain(user) for user in result.scalars()]

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        user = await self._session.get(UserModel, user_id)
        if not user:
            return None

        for key, value in kwargs.items():
            setattr(user, key, value)
        await self._session.commit()
        return self._to_domain(user)

    async def delete_user(self, user_id: int) -> bool:
        user = await self._session.get(UserModel, user_id)
        if not user:
            return False

        await self._session.delete(user)
        await self._session.commit()
        return True

    def _to_domain(self, user: UserModel) -> User:
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            role=UserRole(user.role.value),
            created_at=user.created_at,
            updated_at=user.updated_at
        )
