from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Organization:
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    writers: List['User'] = None  # Связь с писателями
    publications: List['Publication'] = None  # Связь с публикациями
    subscribers: List['TelegramSubscriber'] = None  # Связь с подписчиками

    def __post_init__(self):
        if self.writers is None:
            self.writers = []
        if self.publications is None:
            self.publications = []
        if self.subscribers is None:
            self.subscribers = []

    def add_writer(self, user: 'User') -> None:
        if user not in self.writers:
            self.writers.append(user)
            self.updated_at = datetime.now()

    def remove_writer(self, user: 'User') -> None:
        if user in self.writers:
            self.writers.remove(user)
            self.updated_at = datetime.now()
