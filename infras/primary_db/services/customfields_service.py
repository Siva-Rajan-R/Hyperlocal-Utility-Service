from ..models.base_fields import BaseFields
from sqlalchemy import select,update,delete,and_,or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.service_models.base_service_model import BaseServiceModel
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from schemas.v1.request_schemas.fields_schema import CreateCustomFieldSchema,UpdateCustomFieldSSchema
from schemas.v1.db_schemas.fields_schema import CreateCustomFieldDbSchema,UpdateCustomFieldSDbSchema
from ..repos.customfields_repo import CustomFieldsRepo
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from icecream import ic


class CustomFieldsService(BaseServiceModel):
    def __init__(self, session:AsyncSession):
        self.session=session

    
    async def create(self,data:CreateCustomFieldSchema):
        converted_fields={}
        for field in data.fields:
            converted_fields[field.field_name]={**field.model_dump(mode='json')}

        if len(converted_fields)!=len(data.fields):
            return False
        
        is_service_exists=await self.getby_service_name(service_name=data.service_name,shop_id=data.shop_id)
        ic(is_service_exists)
        if is_service_exists:
            converted_fields_len_before=len(converted_fields)
            converted_fields={**converted_fields,**is_service_exists['fields']}

            ic(converted_fields_len_before)
            ic(len(converted_fields))
            ic(len(is_service_exists['fields']))
            ic(len(is_service_exists['fields'])+converted_fields_len_before)

            if len(converted_fields) != (len(is_service_exists['fields'])+converted_fields_len_before):
                return False
            
            ic("hello")
            return await CustomFieldsRepo(session=self.session).update(is_service_exists['id'],fields=converted_fields,shop_id=data.shop_id)
        
        field_id=generate_uuid()
        data_toadd=CreateCustomFieldDbSchema(
            id=field_id,
            shop_id=data.shop_id,
            service_name=data.service_name,
            fields=converted_fields
        )
        ic("hello")
        ic(data_toadd.id)
        return await CustomFieldsRepo(session=self.session).create(data=data_toadd)

    
    async def update(self,data:UpdateCustomFieldSSchema):
        fields_toupdate=data.fields.model_dump(mode='json',exclude_none=True,exclude_unset=True)
        if not fields_toupdate or len(fields_toupdate)<1:
            return True
        
        data_toupdate=UpdateCustomFieldSDbSchema(id=data.id,shop_id=data.shop_id,field_name=data.field_name,fields=fields_toupdate)
        
        return await CustomFieldsRepo(session=self.session).update_field(data=data_toupdate)
    
    async def delete(self,field_id:str,field_name:str,shop_id:str):
        return await CustomFieldsRepo(session=self.session).delete(field_id=field_id,field_name=field_name,shop_id=shop_id)
    
    async def get(self):
        return await CustomFieldsRepo(session=self.session).get()
    
    async def getby_id(self,field_id:str,shop_id:str):
        return await CustomFieldsRepo(session=self.session).getby_id(field_id=field_id,shop_id=shop_id)
    
    async def getby_service_name(self,service_name:str,shop_id:str):
        return await CustomFieldsRepo(session=self.session).getby_service_name(service_name=service_name,shop_id=shop_id)
    
    async def search(self, query, limit = 5):
        ...


        

    