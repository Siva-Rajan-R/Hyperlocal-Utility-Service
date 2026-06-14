from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from ..main import BASE


class ShopIdConfig(BASE):
    __tablename__ = "shop_id_config"
    id = Column(String, primary_key=True)
    shop_id = Column(String, nullable=False, unique=True, index=True)
    # JSONB blob: { "purchase": {"prefix": "PUR", "start_from": 1}, ... }
    config = Column(JSONB, nullable=False, default={})
