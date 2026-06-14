from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActivityLogSchema(BaseModel):
    shop_id: str
    user_name: str
    service: str
    action: str
    entity_type: str
    entity_id: str
    description: str
    changes: Optional[list[dict]] = []

class GetActivityLogSchema(BaseModel):
    shop_id: str
    limit: int = 50
    offset: int = 0
