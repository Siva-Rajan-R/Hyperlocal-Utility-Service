from typing import Optional

from pydantic import BaseModel, Field


class CreateShopUiIdSchema(BaseModel):
    shop_id: str
    entity_type: str
    prefix: str
    start_from: int = Field(ge=1)
    current_number: int = Field(ge=1)


class UpdateShopUiIdSchema(BaseModel):
    id: str
    shop_id: str

    entity_type: Optional[str] = None
    prefix: Optional[str] = None
    start_from: Optional[int] = Field(default=None, ge=1)
    current_number: Optional[int] = Field(default=None, ge=1)


class DeleteShopUiIdSchema(BaseModel):
    id: str
    shop_id: str


class GetShopUiIdSchema(BaseModel):
    shop_id: str
    offset: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)