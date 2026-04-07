from sqlalchemy import Column,String,Integer,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ..main import BASE


class BaseDropdown(BASE):
    __tablename__="base_dropdown"
    id=Column(String,primary_key=True)
    name=Column(String,nullable=False)
    values=Column(JSONB)