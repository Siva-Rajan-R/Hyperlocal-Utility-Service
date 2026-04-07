from ..models.base_dropdown import BaseDropdown
from sqlalchemy import select,update,delete,and_,or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.service_models.base_service_model import BaseServiceModel
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.request_schemas.dropdown_schema import CreateCustomDropDownValue,UpdateCustomDropDownValue
from schemas.v1.db_schemas.dropdown_schema import CreateCustomDropDownDBValue,UpdateCustomDropDownDbValue
from ..repos.customdropdown_repo import CustomDropDownRepo
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid


class CustomDropDownService(BaseServiceModel):
    def __init__(self, session:AsyncSession):
        self.session=session

    @start_db_transaction
    async def create(self,data:CreateCustomDropDownValue):
        is_dd_exists=await CustomDropDownRepo(session=self.session).getby_name(name=data.dd_name,shop_id=data.shop_id)
        if is_dd_exists:
            return False
        
        dd_id=generate_uuid()
        data_toadd=CreateCustomDropDownDBValue(id=dd_id,values=data.values,shop_id=data.shop_id,name=data.dd_name)
        return await CustomDropDownRepo(session=self.session).create(data=data_toadd)
    
    @start_db_transaction
    async def update(self,data:UpdateCustomDropDownValue):
        data_toupdate=UpdateCustomDropDownDbValue(id=data.id,name=data.dd_name,shop_id=data.shop_id,values=data.values)
        return await CustomDropDownRepo(session=self.session).update(data=data_toupdate)
    
    @start_db_transaction
    async def delete(self,dd_id:str,shop_id:str):
        return await CustomDropDownRepo(session=self.session).delete(dd_id=dd_id,shop_id=shop_id)
    
    async def get(self):
        return await CustomDropDownRepo(session=self.session).get()
    
    async def getby_id(self,dd_id:str,shop_id:str):
        return await CustomDropDownRepo(session=self.session).getby_id(dd_id=dd_id,shop_id=shop_id)
    
    async def search(self, query, limit = 5):
        ...