from fastapi import APIRouter, Depends
from typing import Annotated
from infras.primary_db.main import get_pg_async_session, AsyncSession
from ...handlers.shop_units_handler import ShopUnitHandler
from schemas.v1.request_schemas.shop_unit_schema import CreateShopUnitSchema, UpdateShopUnitSchema, DeleteShopUnitSchema, GetShopUnitSchema

router = APIRouter(
    tags=["Shop Unit CRUD"],
    prefix='/shop-units'
)

PG_SESSION = Annotated[AsyncSession, Depends(get_pg_async_session)]

@router.post('')
async def create(data: CreateShopUnitSchema, session: PG_SESSION):
    return await ShopUnitHandler(session=session).create(data=data)


@router.post('/{shop_id}')
async def init_units(shop_id:str, session: PG_SESSION):
    return await ShopUnitHandler(session=session).init_units(shop_id=shop_id)

@router.put('')
async def update(data: UpdateShopUnitSchema, session: PG_SESSION):
    return await ShopUnitHandler(session=session).update(data=data)

@router.delete('')
async def delete(session: PG_SESSION, data: DeleteShopUnitSchema = Depends()):
    return await ShopUnitHandler(session=session).delete(data=data)

@router.get('')
async def get(session: PG_SESSION, data: GetShopUnitSchema = Depends()):
    return await ShopUnitHandler(session=session).get(data=data)

@router.get('/by/id/{shop_id}/{id}')
async def get_byid(shop_id: str, id: str, session: PG_SESSION):
    return await ShopUnitHandler(session=session).getby_id(id=id, shop_id=shop_id)
