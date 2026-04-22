from fastapi import APIRouter,Depends
from ...handlers.basefields_handler import BaseFieldsHandler,CreateBaseFieldSchema,UpdateBaseFieldSchema
from typing import Annotated
from infras.primary_db.main import get_pg_async_session,AsyncSession


PG_SESSION=Annotated[AsyncSession,Depends(get_pg_async_session)]
SHOP_ID="37d5519b-51a1-5854-982b-4d6524171017"

router=APIRouter(
    tags=[
        "Base Field CRUD"
    ],
    prefix='/fields/base'
)


@router.post('')
async def create(data:CreateBaseFieldSchema,session:PG_SESSION):
    return await BaseFieldsHandler(session=session).create(data=data)

@router.put('')
async def update(data:UpdateBaseFieldSchema,session:PG_SESSION):
    return await BaseFieldsHandler(session=session).update(data=data)

@router.delete('/{field_id}/{field_name}')
async def delete(field_id:str,field_name:str,session:PG_SESSION):
    return await BaseFieldsHandler(session=session).delete(field_id=field_id,field_name=field_name)

@router.get('')
async def get(session:PG_SESSION):
    return await BaseFieldsHandler(session=session).get()

@router.get('/by/id/{field_id}')
async def get_byid(field_id:str,session:PG_SESSION):
    return await BaseFieldsHandler(session=session).getby_id(field_id=field_id)

@router.get('/by/s-name/{service_name}')
async def getby_service_name(service_name:str,session:PG_SESSION):
    return await BaseFieldsHandler(session=session).getby_service_name(service_name=service_name)