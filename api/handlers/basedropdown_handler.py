from sqlalchemy.ext.asyncio import AsyncSession
from hyperlocal_platform.core.models.req_res_models import SuccessResponseTypDict,ErrorResponseTypDict,BaseResponseTypDict
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.request_schemas.dropdown_schema import CreateBaseDropDownValue,UpdateBaseDropDownValue
from schemas.v1.db_schemas.dropdown_schema import CreateBaseDropDownDbValue,UpdateBaseDropDownDbValue
from infras.primary_db.services.basedropdown_service import BaseDropDownService
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from fastapi.exceptions import HTTPException


class BaseDropDownHandler:
    def __init__(self, session:AsyncSession):
        self.session=session

    async def create(self,data:CreateBaseDropDownValue):
        res=await BaseDropDownService(session=self.session).create(data=data)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Dropdown created successfully",
                    status_code=200,
                    success=True
                )
            )
        
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Creating Dropdown",
                description="Invalid data for creating the Dropdown",
                success=False,
                status_code=400
            )
        )
    
    async def update(self,data:UpdateBaseDropDownValue):
        res=await BaseDropDownService(session=self.session).update(data=data)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Dropdown updated successfully",
                    status_code=200,
                    success=True
                )
            )
        
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Updating Dropdown",
                description="Invalid data for updating the Dropdown",
                success=False,
                status_code=400
            )
        )
    
    async def delete(self,dd_id:str):
        res=await BaseDropDownService(session=self.session).delete(dd_id=dd_id)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Dropdown deleted successfully",
                    status_code=200,
                    success=True
                )
            )
        
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Deleting Dropdown",
                description="Invalid data for deleting the Dropdown",
                success=False,
                status_code=400
            )
        )
    
    async def get(self):
        res=await BaseDropDownService(session=self.session).get()
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Dropdown fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
        )
    
    async def getby_id(self,dd_id:str):
        res=await BaseDropDownService(session=self.session).getby_id(dd_id=dd_id)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Field fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
        )