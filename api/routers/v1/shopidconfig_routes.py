from fastapi import APIRouter, Depends
from typing import Annotated
from infras.primary_db.main import get_pg_async_session, AsyncSession
from api.handlers.shopidconfig_handler import ShopIdConfigHandler
from schemas.v1.request_schemas.shopidconfig_schema import UpsertShopIdConfig

PG_SESSION = Annotated[AsyncSession, Depends(get_pg_async_session)]

router = APIRouter(
    tags=["Shop ID Config"],
    prefix="/shop-id-config",
)


@router.get("/{shop_id}")
async def get_config(shop_id: str, session: PG_SESSION):
    return await ShopIdConfigHandler(session=session).get(shop_id=shop_id)


@router.post("")
async def upsert_config(data: UpsertShopIdConfig, session: PG_SESSION):
    return await ShopIdConfigHandler(session=session).upsert(data=data)
