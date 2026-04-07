from pydantic import BaseModel
from core.data_formats.enums.field_enums import FieldTypeEnum
from core.data_formats.basemodels.field_models import FieldModel,UpdateFieldModel
from typing import Optional,List,Union
from core.data_formats.enums.service_enums import ServiceTypeEnum


class CreateBaseFieldSchema(BaseModel):
    service_name:Union[str,ServiceTypeEnum]
    fields:List[FieldModel]

class UpdateBaseFieldSchema(BaseModel):
    id:str
    field_name:str
    fields:UpdateFieldModel


class CreateCustomFieldSchema(BaseModel):
    shop_id:str
    service_name:Union[str,ServiceTypeEnum]
    fields:List[FieldModel]

class UpdateCustomFieldSSchema(BaseModel):
    id:str
    shop_id:str
    field_name:str
    fields:UpdateFieldModel