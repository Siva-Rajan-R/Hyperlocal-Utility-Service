from fastapi import APIRouter,Depends
from ...handlers.customdropdown_handler import CustomDropDownHandler,CreateCustomDropDownValue,UpdateCustomDropDownValue
from typing import Annotated
from infras.primary_db.main import get_pg_async_session,AsyncSession


PG_SESSION=Annotated[AsyncSession,Depends(get_pg_async_session)]
SHOP_ID="37d5519b-51a1-5854-982b-4d6524171017"

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

@router.delete('/{dd_id}')
async def delete(dd_id:str,session:PG_SESSION):
    return await CustomDropDownHandler(session=session).delete(dd_id=dd_id,shop_id=SHOP_ID)

@router.get('')
async def get(session:PG_SESSION):
    return await CustomDropDownHandler(session=session).get()

@router.get('/by/id/{dd_id}')
async def get_byid(dd_id:str,session:PG_SESSION):
    return await CustomDropDownHandler(session=session).getby_id(dd_id=dd_id,shop_id=SHOP_ID)