from fastapi import APIRouter, Depends
from typing import Annotated
from infras.primary_db.main import get_pg_async_session, AsyncSession
from ...handlers.shop_categories_handler import ShopCategoryHandler
from schemas.v1.request_schemas.shop_category_schema import CreateShopCategorySchema, UpdateShopCategorySchema, DeleteShopCategorySchema, GetShopCategorySchema

router = APIRouter(
    tags=["Shop Category CRUD"],
    prefix='/shop-categories'
)

PG_SESSION = Annotated[AsyncSession, Depends(get_pg_async_session)]

@router.post('')
async def create(data: CreateShopCategorySchema, session: PG_SESSION):
    return await ShopCategoryHandler(session=session).create(data=data)

@router.post('/{shop_id}')
async def init_categories(shop_id:str, session: PG_SESSION):
    return await ShopCategoryHandler(session=session).init_categories(shop_id=shop_id)

@router.put('')
async def update(data: UpdateShopCategorySchema, session: PG_SESSION):
    return await ShopCategoryHandler(session=session).update(data=data)

@router.delete('')
async def delete(session: PG_SESSION, data: DeleteShopCategorySchema = Depends()):
    return await ShopCategoryHandler(session=session).delete(data=data)

@router.get('')
async def get(session: PG_SESSION, data: GetShopCategorySchema = Depends()):
    return await ShopCategoryHandler(session=session).get(data=data)

@router.get('/by/id/{shop_id}/{id}')
async def get_byid(shop_id: str, id: str, session: PG_SESSION):
    return await ShopCategoryHandler(session=session).getby_id(id=id, shop_id=shop_id)
