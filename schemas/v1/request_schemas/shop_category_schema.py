from pydantic import BaseModel, Field
from typing import Optional

class CreateShopCategorySchema(BaseModel):
    shop_id: str
    name: str
    description: Optional[str] = None
    is_active: bool = True

class UpdateShopCategorySchema(BaseModel):
    id: str
    shop_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class DeleteShopCategorySchema(BaseModel):
    id: str
    shop_id: str

class GetShopCategorySchema(BaseModel):
    shop_id: str
    limit: int = Field(default=10, le=100)
    offset: int = Field(default=1)
