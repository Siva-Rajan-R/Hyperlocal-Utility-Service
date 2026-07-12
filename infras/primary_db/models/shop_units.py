from sqlalchemy import Column, String, Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from ..main import BASE

class ShopUnits(BASE):
    __tablename__ = "shop_units"
    
    id = Column(String, primary_key=True)
    shop_id = Column(String, nullable=False, index=True) # "DEFAULT" for global defaults
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    description = Column(String)
    is_default = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    sub_units = Column(JSONB, nullable=True, default=list)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )
