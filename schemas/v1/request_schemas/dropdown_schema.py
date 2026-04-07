from pydantic import BaseModel
from typing import List,Optional


class CreateBaseDropDownValue(BaseModel):
    dd_name:str
    values:List[str]

class UpdateBaseDropDownValue(BaseModel):
    id:str
    dd_name:str
    values:Optional[List[str]]=None


class CreateCustomDropDownValue(BaseModel):
    shop_id:str
    dd_name:str
    values:List[str]

class UpdateCustomDropDownValue(BaseModel):
    id:str
    shop_id:str
    dd_name:str
    values:Optional[List[str]]=None

