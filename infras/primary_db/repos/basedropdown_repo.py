from ..models.base_dropdown import BaseDropdown
from sqlalchemy import select,update,delete,and_,or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.repo_models.base_repo_model import BaseRepoModel
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.db_schemas.dropdown_schema import CreateBaseDropDownDbValue,UpdateBaseDropDownDbValue


class BaseDropDownRepo(BaseRepoModel):
    def __init__(self, session:AsyncSession):
        self.session=session

    @start_db_transaction
    async def create(self,data:CreateBaseDropDownDbValue):
        self.session.add(BaseDropdown(**data.model_dump(mode='json')))

        return True
    
    @start_db_transaction
    async def update(self,data:UpdateBaseDropDownDbValue):
        data_toupdate=update(
            BaseDropdown
        ).where(
            BaseDropdown.id==data.id,
            BaseDropdown.name==data.name
        ).values(
            values=data.values
        ).returning(BaseDropdown.id)

        is_updated=(await self.session.execute(data_toupdate)).scalar_one_or_none()

        return is_updated
    
    @start_db_transaction
    async def delete(self,dd_id:str):
        data_todel=delete(
            BaseDropdown
        ).where(
            BaseDropdown.id==dd_id
        ).returning(BaseDropdown.id)

        is_deleted=(await self.session.execute(data_todel)).scalar_one_or_none()

        return is_deleted
    
    async def get(self):
        dd_toget_stmt=select(
            BaseDropdown.id,
            BaseDropdown.name,
            BaseDropdown.values
        )

        dropdowns=(await self.session.execute(dd_toget_stmt)).mappings().all()

        return dropdowns
    
    async def getby_id(self,dd_id:str):
        dd_toget_stmt=select(
            BaseDropdown.id,
            BaseDropdown.name,
            BaseDropdown.values
        ).where(
            BaseDropdown.id==dd_id
        )

        dropdown=(await self.session.execute(dd_toget_stmt)).mappings().one_or_none()

        return dropdown
    
    async def getby_name(self,name:str):
        dd_toget_stmt=select(
            BaseDropdown.id,
            BaseDropdown.name,
            BaseDropdown.values
        ).where(
            BaseDropdown.name==name
        )

        dropdown=(await self.session.execute(dd_toget_stmt)).mappings().one_or_none()

        return dropdown
    
    async def search(self, query, limit = 5):
        ...