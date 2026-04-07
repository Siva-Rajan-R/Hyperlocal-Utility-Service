from ..models.base_dropdown import BaseDropdown
from sqlalchemy import select,update,delete,and_,or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.service_models.base_service_model import BaseServiceModel
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.request_schemas.dropdown_schema import CreateBaseDropDownValue,UpdateBaseDropDownValue
from schemas.v1.db_schemas.dropdown_schema import CreateBaseDropDownDbValue,UpdateBaseDropDownDbValue
from ..repos.basedropdown_repo import BaseDropDownRepo
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid


class BaseDropDownService(BaseServiceModel):
    def __init__(self, session:AsyncSession):
        self.session=session

    @start_db_transaction
    async def create(self,data:CreateBaseDropDownValue):
        is_dd_exists=await BaseDropDownRepo(session=self.session).getby_name(name=data.dd_name)
        if is_dd_exists:
            return False
        
        dd_id=generate_uuid()
        data_toadd=CreateBaseDropDownDbValue(id=dd_id,values=data.values,name=data.dd_name)
        return await BaseDropDownRepo(session=self.session).create(data=data_toadd)
    
    @start_db_transaction
    async def update(self,data:UpdateBaseDropDownValue):
        data_toupdate=UpdateBaseDropDownDbValue(id=data.id,name=data.dd_name,values=data.values)
        return await BaseDropDownRepo(session=self.session).update(data=data_toupdate)
    
    @start_db_transaction
    async def delete(self,dd_id:str):
        return await BaseDropDownRepo(session=self.session).delete(dd_id=dd_id)
    
    async def get(self):
        return await BaseDropDownRepo(session=self.session).get()
    
    async def getby_id(self,dd_id:str):
        return await BaseDropDownRepo(session=self.session).getby_id(dd_id=dd_id)
    
    async def search(self, query, limit = 5):
        ...