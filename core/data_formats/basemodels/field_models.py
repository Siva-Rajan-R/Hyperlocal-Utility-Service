from pydantic import BaseModel
from core.data_formats.enums.field_enums import FieldTypeEnum
from typing import Optional
from ..enums.field_enums import ViewModeEnum

class FieldModel(BaseModel):
    field_name:str
    field_description:str
    label_name:str
    placeholder:str
    type:FieldTypeEnum
    required:bool
    category:str
    category_description:str
    can_update:bool
    view_mode:ViewModeEnum
    conn_id:Optional[str]=None

class UpdateFieldModel(BaseModel):
    field_description:str
    label_name:str
    placeholder:str
    required:bool
    category:str
    category_description:str
    can_update:bool
    view_mode:ViewModeEnum
    conn_id:Optional[str]=None