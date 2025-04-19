from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..domain import Tag, Publication, User, Organization #, TelegramSubscriber


class UserRepositoryPort(ABC):
    @abstractmethod
    async def create_user(self, username: str, email: str, password_hash: str, role: str) -> Optional[User]: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]: ...

    @abstractmethod
    async def get_all_users(self) -> List[User]: ...

    @abstractmethod
    async def update_user(self, user_id: int, **kwargs: Any) -> Optional[User]: ...

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool: ...


class OrganizationRepositoryPort(ABC):
    @abstractmethod
    async def create_organization(self, name: str, description: Optional[str] = None,
                                  logo_url: Optional[str] = None) -> Optional[Organization]: ...

    @abstractmethod
    async def get_organization_by_id(self, org_id: int) -> Optional[Organization]: ...

    @abstractmethod
    async def get_all_organizations(self) -> List[Organization]: ...

    @abstractmethod
    async def update_organization(self, org_id: int, **kwargs: Any) -> Optional[Organization]: ...

    @abstractmethod
    async def delete_organization(self, org_id: int) -> bool: ...

    @abstractmethod
    async def add_writer(self, writer_id: int, organization_id: int) -> bool: ...

    @abstractmethod
    async def remove_writer(self, writer_id: int, organization_id: int) -> bool: ...

    @abstractmethod
    async def get_organization_writers(self, org_id: int) -> List[User]: ...


class TagRepositoryPort(ABC):
    @abstractmethod
    async def create_tag(self, name: str) -> Optional[Tag]: ...

    @abstractmethod
    async def get_tag_by_id(self, tag_id: int) -> Optional[Tag]: ...

    @abstractmethod
    async def get_tag_by_name(self, name: str) -> Optional[Tag]: ...

    @abstractmethod
    async def get_all_tags(self) -> List[Tag]: ...

    @abstractmethod
    async def delete_tag(self, tag_id: int) -> bool: ...


class PublicationRepositoryPort(ABC):
    @abstractmethod
    async def create_publication(
            self,
            title: str,
            content: str,
            writer_id: int,
            organization_id: int,
            publish_date: datetime,
            featured_image_url: Optional[str] = None,
            event_start_date: Optional[datetime] = None,
            event_end_date: Optional[datetime] = None,
            is_archived: bool = False,
            tags: Optional[List[str]] = None
    ) -> Optional[Publication]: ...

    @abstractmethod
    async def get_publication_by_id(self, pub_id: int) -> Optional[Publication]: ...

    @abstractmethod
    async def get_all_publications(self) -> List[Publication]: ...

    @abstractmethod
    async def get_publications_by_organization(self, org_id: int) -> List[Publication]: ...

    @abstractmethod
    async def get_publications_by_writer(self, writer_id: int) -> List[Publication]: ...

    @abstractmethod
    async def get_publications_by_tag(self, tag_name: str) -> List[Publication]: ...

    @abstractmethod
    async def update_publication(self, pub_id: int, **kwargs: Any) -> Optional[Publication]: ...

    @abstractmethod
    async def delete_publication(self, pub_id: int) -> bool: ...

    @abstractmethod
    async def add_tag_to_publication(self, publication_id: int, tag_id: int) -> bool: ...

    @abstractmethod
    async def remove_tag_from_publication(self, publication_id: int, tag_id: int) -> bool: ...


class TelegramSubscriberRepositoryPort(ABC):
    @abstractmethod
    async def create_subscriber(self, chat_id: int, username: Optional[str] = None) -> Optional[TelegramSubscriber]: ...

    @abstractmethod
    async def get_subscriber_by_chat_id(self, chat_id: int) -> Optional[TelegramSubscriber]: ...

    @abstractmethod
    async def update_subscriber(self, chat_id: int, **kwargs: Any) -> Optional[TelegramSubscriber]: ...

    @abstractmethod
    async def delete_subscriber(self, chat_id: int) -> bool: ...

    @abstractmethod
    async def subscribe_to_organization(self, chat_id: int, org_id: int) -> bool: ...

    @abstractmethod
    async def unsubscribe_from_organization(self, chat_id: int, org_id: int) -> bool: ...

    @abstractmethod
    async def get_subscriber_organizations(self, chat_id: int) -> List[Organization]: ...

    @abstractmethod
    async def get_organization_subscribers(self, org_id: int) -> List[TelegramSubscriber]: ...