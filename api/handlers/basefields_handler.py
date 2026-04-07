from sqlalchemy import select,update,delete,and_,or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.repo_models.base_repo_model import BaseRepoModel
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.request_schemas.fields_schema import CreateBaseFieldSchema,UpdateBaseFieldSchema
from schemas.v1.db_schemas.fields_schema import CreateBaseFieldDbSchema,UpdateBaseFieldSDbSchema
from infras.primary_db.services.basefields_service import BaseFieldsService
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from hyperlocal_platform.core.models.req_res_models import SuccessResponseTypDict,ErrorResponseTypDict,BaseResponseTypDict
from fastapi import HTTPException
from core.data_formats.enums.service_enums import ServiceTypeEnum
from icecream import ic


class BaseFieldsHandler:
    def __init__(self, session:AsyncSession):
        self.session=session

    async def create(self,data:CreateBaseFieldSchema):
        res=await BaseFieldsService(session=self.session).create(data=data)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Field created successfully",
                    status_code=200,
                    success=True
                )
            )
        
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Creating field",
                description="Invalid data for creating the field",
                success=False,
                status_code=400
            )
        )

    async def update(self,data:UpdateBaseFieldSchema):
        res=await BaseFieldsService(session=self.session).update(data=data)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Field update successfully",
                    status_code=200,
                    success=True
                )
            )
        
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Updating field",
                description="Invalid data for updating the field",
                success=False,
                status_code=400
            )
        )
    
    async def delete(self,field_id:str,field_name:str):
        res=await BaseFieldsService(session=self.session).delete(field_id=field_id,field_name=field_name)
        if res:
            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Field deleted successfully",
                    status_code=200,
                    success=True
                )
            )
        
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error - Deleting field",
                description="Invalid data for deleting the field",
                success=False,
                status_code=400
            )
        )
    
    async def get(self):
        res=await BaseFieldsService(session=self.session).get()
        ic(res)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Field fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
        )
    
    async def getby_id(self,field_id:str):
        res=await BaseFieldsService(session=self.session).getby_id(field_id=field_id)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Field fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
        )
    
    async def getby_service_name(self,service_name:ServiceTypeEnum):
        res= await BaseFieldsService(session=self.session).getby_service_name(service_name=service_name)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Field fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
        )


        

    