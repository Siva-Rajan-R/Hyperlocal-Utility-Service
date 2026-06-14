from pydantic import BaseModel
from typing import Dict, Optional


class ModuleIdConfig(BaseModel):
    prefix: str
    start_from: int = 1


class UpsertShopIdConfig(BaseModel):
    shop_id: str
    config: Dict[str, ModuleIdConfig]
