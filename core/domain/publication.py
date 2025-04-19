from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


@dataclass
class Publication:
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    featured_image_url: Optional[str] = None
    writer_id: Optional[int] = None
    organization: Optional['Organization'] = None  # Мейби тут что-то
    publish_date: datetime = datetime.now()
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    is_archived: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    tags: List['Tag'] = None  # Связь с тегами через композицию

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "featured_image_url": self.featured_image_url,
            "writer_id": self.writer_id,
            "organization": self.organization,
            "publish_date": self.publish_date.isoformat() if self.publish_date else None,
            "event_start_date": self.event_start_date.isoformat() if self.event_start_date else None,
            "event_end_date": self.event_end_date.isoformat() if self.event_end_date else None,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "tags": [tag.to_dict() for tag in self.tags] if self.tags else []
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    def __str__(self):
        return f"{self.title}\n{self.content}"
