from pydantic import BaseModel, Field
from typing import Optional

class CreateShopUnitSchema(BaseModel):
    shop_id: str
    name: str
    short_name: str
    description: Optional[str] = None
    is_active: bool = True

class UpdateShopUnitSchema(BaseModel):
    id: str
    shop_id: str
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class DeleteShopUnitSchema(BaseModel):
    id: str
    shop_id: str

class GetShopUnitSchema(BaseModel):
    shop_id: str
    limit: int = Field(default=10, le=100)
    offset: int = Field(default=1)
