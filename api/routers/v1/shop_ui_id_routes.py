from typing import Annotated

from fastapi import APIRouter, Depends

from infras.primary_db.main import AsyncSession, get_pg_async_session
from ...handlers.shop_ui_id_handler import ShopUiIdHandler

from schemas.v1.request_schemas.shop_ui_id_schema import (
    CreateShopUiIdSchema,
    UpdateShopUiIdSchema,
    DeleteShopUiIdSchema,
    GetShopUiIdSchema,
)

router = APIRouter(
    tags=["Shop UI ID CRUD"],
    prefix="/shop-ui-ids",
)

PG_SESSION = Annotated[AsyncSession, Depends(get_pg_async_session)]


@router.post("")
async def create(
    data: CreateShopUiIdSchema,
    session: PG_SESSION,
):
    return await ShopUiIdHandler(session=session).create(data=data)


@router.post('/{shop_id}')
async def init_ids(shop_id:str, session: PG_SESSION):
    return await ShopUiIdHandler(session=session).init_ids(shop_id=shop_id)


@router.put("")
async def update(
    data: UpdateShopUiIdSchema,
    session: PG_SESSION,
):
    return await ShopUiIdHandler(session=session).update(data=data)


@router.delete("")
async def delete(
    session: PG_SESSION,
    data: DeleteShopUiIdSchema = Depends(),
):
    return await ShopUiIdHandler(session=session).delete(data=data)


@router.get("")
async def get(
    session: PG_SESSION,
    data: GetShopUiIdSchema = Depends(),
):
    return await ShopUiIdHandler(session=session).get(data=data)


@router.get("/by/id/{shop_id}/{id}")
async def get_by_id(
    shop_id: str,
    id: str,
    session: PG_SESSION,
):
    return await ShopUiIdHandler(session=session).getby_id(
        id=id,
        shop_id=shop_id,
    )


@router.get("/by/entity/{shop_id}/{entity_type}")
async def get_by_entity_type(
    shop_id: str,
    entity_type: str,
    session: PG_SESSION,
):
    return await ShopUiIdHandler(session=session).get_by_entity_type(
        shop_id=shop_id,
        entity_type=entity_type,
    )


@router.get("/next/{shop_id}/{entity_type}")
async def get_next_number(
    shop_id: str,
    entity_type: str,
    session: PG_SESSION,
):
    return await ShopUiIdHandler(session=session).get_next_number(
        shop_id=shop_id,
        entity_type=entity_type,
    )