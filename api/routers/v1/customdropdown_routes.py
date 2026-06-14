from fastapi import APIRouter,Depends
from ...handlers.customdropdown_handler import CustomDropDownHandler,CreateCustomDropDownValue,UpdateCustomDropDownValue
from typing import Annotated
from infras.primary_db.main import get_pg_async_session,AsyncSession


PG_SESSION=Annotated[AsyncSession,Depends(get_pg_async_session)]

router=APIRouter(
    tags=[
        "Custom DropDown CRUD"
    ],
    prefix='/dropdowns/custom'
)


@router.post('')
async def create(data:CreateCustomDropDownValue,session:PG_SESSION):
    return await CustomDropDownHandler(session=session).create(data=data)

@router.put('')
async def update(data:UpdateCustomDropDownValue,session:PG_SESSION):
    return await CustomDropDownHandler(session=session).update(data=data)

@router.delete('/{dd_id}/{shop_id}')
async def delete(dd_id:str,shop_id:str,session:PG_SESSION):
    return await CustomDropDownHandler(session=session).delete(dd_id=dd_id,shop_id=shop_id)

@router.get('')
async def get(session:PG_SESSION):
    return await CustomDropDownHandler(session=session).get()

@router.get('/by/shop/{shop_id}')
async def get_by_shop(shop_id:str,session:PG_SESSION):
    return await CustomDropDownHandler(session=session).get_by_shop(shop_id=shop_id)

@router.get('/by/name/{shop_id}/{name}')
async def get_by_name(shop_id:str,name:str,session:PG_SESSION):
    return await CustomDropDownHandler(session=session).get_by_name(shop_id=shop_id,name=name)

@router.get('/by/id/{dd_id}')
async def get_byid(dd_id:str,session:PG_SESSION):
    return await CustomDropDownHandler(session=session).getby_id(dd_id=dd_id,shop_id=dd_id)