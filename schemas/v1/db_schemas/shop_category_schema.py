from pydantic import BaseModel
from typing import Optional

class CreateShopCategoryDbSchema(BaseModel):
    id: str
    shop_id: str
    name: str
    description: Optional[str] = None
    is_default: bool = False
    is_active: bool = True

class UpdateShopCategoryDbSchema(BaseModel):
    id: str
    shop_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
