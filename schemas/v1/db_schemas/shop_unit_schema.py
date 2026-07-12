from pydantic import BaseModel
from typing import Optional, List

class CreateShopUnitDbSchema(BaseModel):
    id: str
    shop_id: str
    name: str
    short_name: str
    description: Optional[str] = None
    is_default: bool = False
    is_active: bool = True
    sub_units: Optional[List[dict]] = None

class UpdateShopUnitDbSchema(BaseModel):
    id: str
    shop_id: str
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sub_units: Optional[List[dict]] = None
