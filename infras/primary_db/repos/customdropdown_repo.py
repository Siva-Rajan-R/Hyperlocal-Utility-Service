from ..models.custom_dropdown import CustomDropdown
from sqlalchemy import select,update,delete,and_,or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.repo_models.base_repo_model import BaseRepoModel
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.db_schemas.dropdown_schema import CreateCustomDropDownDBValue,UpdateCustomDropDownDbValue


class CustomDropDownRepo(BaseRepoModel):
    def __init__(self, session:AsyncSession):
        self.session=session

    @start_db_transaction
    async def create(self,data:CreateCustomDropDownDBValue):
        self.session.add(CustomDropdown(**data.model_dump(mode='json')))

        return True
    
    @start_db_transaction
    async def update(self,data:UpdateCustomDropDownDbValue):
        data_toupdate=update(
            CustomDropdown
        ).where(
            CustomDropdown.id==data.id,
            CustomDropdown.name==data.name
        ).values(
            values=data.values
        ).returning(CustomDropdown.id)

        is_updated=(await self.session.execute(data_toupdate)).scalar_one_or_none()

        return is_updated
    
    @start_db_transaction
    async def delete(self,dd_id:str,shop_id:str):
        data_todel=delete(
            CustomDropdown
        ).where(
            CustomDropdown.id==dd_id,
            CustomDropdown.shop_id==shop_id
        ).returning(CustomDropdown.id)

        is_deleted=(await self.session.execute(data_todel)).scalar_one_or_none()

        return is_deleted
    
    async def get(self):
        dd_toget_stmt=select(
            CustomDropdown.id,
            CustomDropdown.shop_id,
            CustomDropdown.name,
            CustomDropdown.values
        )

        dropdowns=(await self.session.execute(dd_toget_stmt)).mappings().all()

        return dropdowns
    
    async def getby_id(self,dd_id:str,shop_id:str):
        dd_toget_stmt=select(
            CustomDropdown.id,
            CustomDropdown.shop_id,
            CustomDropdown.name,
            CustomDropdown.values
        ).where(
            CustomDropdown.id==dd_id,
            CustomDropdown.shop_id==shop_id
        )

        dropdown=(await self.session.execute(dd_toget_stmt)).mappings().one_or_none()

        return dropdown
    
    async def getby_name(self,name:str,shop_id:str):
        dd_toget_stmt=select(
            CustomDropdown.id,
            CustomDropdown.shop_id,
            CustomDropdown.name,
            CustomDropdown.values
        ).where(
            CustomDropdown.name==name,
            CustomDropdown.shop_id==shop_id
        )

        dropdown=(await self.session.execute(dd_toget_stmt)).mappings().one_or_none()

        return dropdown
    
    async def search(self, query, limit = 5):
        ...