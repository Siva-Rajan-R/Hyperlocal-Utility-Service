from sqlalchemy.ext.asyncio import AsyncSession
from hyperlocal_platform.core.models.req_res_models import (
    SuccessResponseTypDict, ErrorResponseTypDict, BaseResponseTypDict
)
from fastapi.exceptions import HTTPException
from infras.primary_db.services.shopidconfig_service import ShopIdConfigService
from schemas.v1.request_schemas.shopidconfig_schema import UpsertShopIdConfig
from messaging.main import RabbitMQMessagingConfig
from icecream import ic


class ShopIdConfigHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, shop_id: str):
        res = await ShopIdConfigService(session=self.session).get(shop_id=shop_id)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Shop ID config fetched successfully",
                status_code=200,
                success=True,
            ),
            data=res,
        )

    async def upsert(self, data: UpsertShopIdConfig):
        res = await ShopIdConfigService(session=self.session).upsert(
            shop_id=data.shop_id,
            config={k: v.model_dump() for k, v in data.config.items()},
        )
        if res:
            # Publish event to RabbitMQ
            try:
                await RabbitMQMessagingConfig().publish_event(
                    routing_key="hyperlocal.shopconfig.updated",
                    payload={
                        "shop_id": data.shop_id,
                        "config": {k: v.model_dump() for k, v in data.config.items()}
                    },
                    headers={},
                    exchange_name="hyperlocal_domain_events"
                )
            except Exception as e:
                ic(f"Failed to publish shop config event: {e}")

            return SuccessResponseTypDict(
                detail=BaseResponseTypDict(
                    msg="Shop ID config saved successfully",
                    status_code=200,
                    success=True,
                )
            )
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseTypDict(
                msg="Error saving shop ID config",
                description="Invalid data",
                success=False,
                status_code=400,
            ),
        )
