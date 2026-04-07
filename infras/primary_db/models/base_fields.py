from sqlalchemy import Column,String,Integer,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ..main import BASE


class BaseFields(BASE):
    __tablename__="base_fields"
    id=Column(String,primary_key=True)
    service_name=Column(String,unique=True,nullable=False)
    fields=Column(JSONB)