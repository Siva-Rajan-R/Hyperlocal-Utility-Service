from sqlalchemy import Column, String, Boolean, TIMESTAMP, func,BigInteger
from ..main import BASE

class ShopUiId(BASE):
    __tablename__ = "shop_ui_id"
    
    id = Column(String, primary_key=True)
    shop_id = Column(String, nullable=False, index=True) # "DEFAULT" for global defaults
    entity_type = Column(String, nullable=False)
    prefix = Column(String, nullable=False)
    start_from=Column(BigInteger)
    current_number=Column(BigInteger)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )
