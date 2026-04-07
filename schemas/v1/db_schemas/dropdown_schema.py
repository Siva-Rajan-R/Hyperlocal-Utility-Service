from pydantic import BaseModel
from typing import List,Optional


class CreateBaseDropDownDbValue(BaseModel):
    id:str
    name:str
    values:List[str]

class UpdateBaseDropDownDbValue(BaseModel):
    id:str
    name:str
    values:Optional[List[str]]=None


class CreateCustomDropDownDBValue(BaseModel):
    id:str
    shop_id:str
    name:str
    values:List[str]

class UpdateCustomDropDownDbValue(BaseModel):
    id:str
    shop_id:str
    name:str
    values:Optional[List[str]]=None

