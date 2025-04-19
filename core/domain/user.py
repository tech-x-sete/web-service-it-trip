from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    MODERATOR = "moderator"
    WRITER = "writer"
    GUEST = "guest"  # Удалить нахрен эту роль


@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    login: str = ""
    password_hash: str = ""
    role: UserRole = UserRole.GUEST
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    organizations: List['Organization'] = None  # Связь с организациями
    publications: List['Publication'] = None  # Связь с публикациями

    def __post_init__(self):
        if self.organizations is None:
            self.organizations = []
        if self.publications is None:
            self.publications = []

    def is_moderator(self) -> bool:
        return self.role == UserRole.MODERATOR

    def change_role(self, new_role: UserRole) -> None:
        self.role = new_role
        self.updated_at = datetime.now()
