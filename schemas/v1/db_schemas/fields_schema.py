from pydantic import BaseModel
from core.data_formats.basemodels.field_models import FieldModel,UpdateFieldModel
from typing import Optional,List,Union
from core.data_formats.enums.service_enums import ServiceTypeEnum


class CreateBaseFieldDbSchema(BaseModel):
    id:str
    service_name:Union[str,ServiceTypeEnum]
    fields:dict
    

class UpdateBaseFieldSDbSchema(BaseModel):
    id:str
    field_name:str
    fields:dict

class CreateCustomFieldDbSchema(BaseModel):
    id:str
    shop_id:str
    service_name:Union[str,ServiceTypeEnum]
    fields:dict

class UpdateCustomFieldSDbSchema(BaseModel):
    id:str
    shop_id:str
    field_name:str
    fields:dict
