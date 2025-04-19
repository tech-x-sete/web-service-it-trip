from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Publication:
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    featured_image_url: Optional[str] = None
    writer_id: Optional[int] = None
    organization_id: Optional[int] = None
    publish_date: datetime = datetime.now()
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    is_archived: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    tags: List['Tag'] = None  # Связь с тегами через композицию

    def __str__(self):
        ...
