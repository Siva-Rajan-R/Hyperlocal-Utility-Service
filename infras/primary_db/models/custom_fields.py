from sqlalchemy import Column,String,Integer,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ..main import BASE


class CustomFields(BASE):
    __tablename__="custom_fields"
    id=Column(String,primary_key=True)
    shop_id=Column(String,nullable=False)
    service_name=Column(String,nullable=False)
    fields=Column(JSONB)