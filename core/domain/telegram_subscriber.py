from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class TelegramSubscriber:
    id: Optional[int] = None
    chat_id: int = 0
    username: Optional[str] = None
    subscribed_at: datetime = datetime.now()
    subscriptions: List['Organization'] = None  # Связь с организациями

    def __post_init__(self):
        if self.subscriptions is None:
            self.subscriptions = []

    def subscribe(self, organization: 'Organization') -> None:
        if organization not in self.subscriptions:
            self.subscriptions.append(organization)

    def unsubscribe(self, organization: 'Organization') -> None:
        if organization in self.subscriptions:
            self.subscriptions.remove(organization)