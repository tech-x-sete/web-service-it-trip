from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Tag:
    id: Optional[int] = None
    name: str = ""
    created_at: datetime = datetime.now()
    publications: List['Publication'] = None
