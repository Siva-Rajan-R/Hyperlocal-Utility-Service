from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class ActivityLogReadModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    shop_id: str
    user_name: str
    service: str
    action: str
    entity_type: str
    entity_id: str
    description: str
    changes: Optional[list[dict]] = []
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
