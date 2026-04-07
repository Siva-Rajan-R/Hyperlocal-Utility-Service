from sqlalchemy import Column,String,Integer,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ..main import BASE


class CustomDropdown(BASE):
    __tablename__="custom_dropdown"
    id=Column(String,primary_key=True)
    shop_id=Column(String,nullable=False)
    name=Column(String,nullable=False)
    values=Column(JSONB)