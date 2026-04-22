from fastapi import APIRouter,Depends
from ...handlers.basedropdown_handler import BaseDropDownHandler,CreateBaseDropDownValue,UpdateBaseDropDownValue
from typing import Annotated
from infras.primary_db.main import get_pg_async_session,AsyncSession


PG_SESSION=Annotated[AsyncSession,Depends(get_pg_async_session)]
SHOP_ID="37d5519b-51a1-5854-982b-4d6524171017"

router=APIRouter(
    tags=[
        "Base DropDown CRUD"
    ],
    prefix='/dropdowns/base'
)


@router.post('')
async def create(data:CreateBaseDropDownValue,session:PG_SESSION):
    return await BaseDropDownHandler(session=session).create(data=data)

@router.put('')
async def update(data:UpdateBaseDropDownValue,session:PG_SESSION):
    return await BaseDropDownHandler(session=session).update(data=data)

@router.delete('/{dd_id}')
async def delete(dd_id:str,session:PG_SESSION):
    return await BaseDropDownHandler(session=session).delete(dd_id=dd_id)

@router.get('')
async def get(session:PG_SESSION):
    return await BaseDropDownHandler(session=session).get()

@router.get('/by/id/{dd_id}')
async def get_byid(dd_id:str,session:PG_SESSION):
    return await BaseDropDownHandler(session=session).getby_id(dd_id=dd_id)