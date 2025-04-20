from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class Publication:
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    featured_image_url: Optional[str] = None
    writer_id: Optional[int] = None
    organization: Optional['Organization'] = None  # Мейби тут что-то
    publish_date: datetime = datetime.now()
    event_date: Optional[datetime] = None
    is_archived: bool = False
    created_at: datetime = datetime.now()
    location: str = ""

    def __str__(self):
        return f"{self.title}\n{self.content}"
