from sqlalchemy import Column, String, Boolean, TIMESTAMP, func
from ..main import BASE

class ShopCategories(BASE):
    __tablename__ = "shop_categories"
    
    id = Column(String, primary_key=True)
    shop_id = Column(String, nullable=False, index=True) # "DEFAULT" for global defaults
    name = Column(String, nullable=False)
    description = Column(String)
    is_default = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )
