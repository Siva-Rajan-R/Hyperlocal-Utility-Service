from sqlalchemy.ext.asyncio import AsyncSession
from models.service_models.base_service_model import BaseServiceModel

from schemas.v1.request_schemas.shop_ui_id_schema import (
    CreateShopUiIdSchema,
    UpdateShopUiIdSchema,
    DeleteShopUiIdSchema,
    GetShopUiIdSchema,
)

from schemas.v1.db_schemas.shop_ui_id_schema import (
    CreateShopUiIdDbSchema,
    UpdateShopUiIdDbSchema,
)

from ..repos.shop_ui_id_repo import ShopUiIdRepo
from ..models.shop_ui_id import ShopUiId

from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from messaging.main import RabbitMQMessagingConfig

from datetime import datetime, timezone

from hyperlocal_platform.core.utils.activity_logger import ActivityLogger
from core.constants import DEFAULT_UI_IDS
from icecream import ic

class ShopUiIdService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ShopUiIdRepo(session=session)
        self.msg_config = RabbitMQMessagingConfig()

    async def _emit_event(self, action: str, id: str, shop_id: str):
        payload = {
            "entity": "ShopUiId",
            "action": action,
            "id": id,
            "shop_id": shop_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        headers = {
            "routing_key": f"utility.shop_ui_id.{action.lower()}",
            "exchange_name": "utility_exchange",
            "entity_name": "shop_ui_id",
            "service_name": "UTILITY",
            "saga_id": "none",
            "reply_key": "none",
            "reply_exchange": "none",
            "reply_entity_name": "none",
            "body": payload,
        }

        await self.msg_config.publish_event(
            routing_key=headers["routing_key"],
            exchange_name=headers["exchange_name"],
            payload=payload,
            headers=headers,
        )

    async def init_ids(self, shop_id: str):
        data = []
        DEFAULT_START_NUMBER=100000
        for item in DEFAULT_UI_IDS:
            ic(item)
            data.append(
                ShopUiId(
                    id=generate_uuid(),
                    shop_id=shop_id,
                    entity_type=item["entity_type"],
                    prefix=item["prefix"],
                    start_from=DEFAULT_START_NUMBER,
                    current_number=DEFAULT_START_NUMBER,
                )
            )
        ic(data)
        res = await self.repo.create_bulk(data=data)
        ic(res)

        return res

    async def create(self, data: CreateShopUiIdSchema):
        id = generate_uuid()

        db_data = CreateShopUiIdDbSchema(
            id=id,
            **data.model_dump(),
        )

        res = await self.repo.create(data=db_data)

        if res:
            await self._emit_event("CREATED", id, data.shop_id)

            await ActivityLogger.log(
                shop_id=data.shop_id,
                service="Utility",
                action="CREATE",
                entity_type="ShopUiId",
                entity_id=id,
                description=f"Created Shop UI ID for {data.entity_type}",
                changes=[
                    {
                        "field": "entity_type",
                        "before": "",
                        "after": data.entity_type,
                    }
                ],
            )

        return res

    async def update(self, data: UpdateShopUiIdSchema):
        old_data = await self.repo.getby_id(
            id=data.id,
            shop_id=data.shop_id,
        )

        res = await self.repo.update(
            data=UpdateShopUiIdDbSchema(
                **data.model_dump(exclude_unset=True)
            )
        )

        if res and old_data:
            await self._emit_event("UPDATED", data.id, data.shop_id)

            changes = ActivityLogger.compute_changes(
                old_data,
                data.model_dump(
                    exclude_none=True,
                    exclude_unset=True,
                ),
            )

            if changes:
                desc_changes = [
                    f"{c['field']} prv({c['before']}) after ({c['after']})"
                    for c in changes
                ]

                await ActivityLogger.log(
                    shop_id=data.shop_id,
                    service="Utility",
                    action="UPDATE",
                    entity_type="ShopUiId",
                    entity_id=data.id,
                    description=f"Updated Shop UI ID {', '.join(desc_changes)}",
                    changes=changes,
                )

        return res

    async def delete(self, data: DeleteShopUiIdSchema):
        old_data = await self.repo.getby_id(
            id=data.id,
            shop_id=data.shop_id,
        )

        res = await self.repo.delete(data=data)

        if res:
            await self._emit_event("DELETED", data.id, data.shop_id)

            entity = (
                old_data.get("entity_type", "Unknown")
                if old_data
                else "Unknown"
            )

            await ActivityLogger.log(
                shop_id=data.shop_id,
                service="Utility",
                action="DELETE",
                entity_type="ShopUiId",
                entity_id=data.id,
                description=f"Deleted Shop UI ID for {entity}",
                changes=[
                    {
                        "field": "entity_type",
                        "before": entity,
                        "after": "DELETED",
                    }
                ],
            )

        return res

    async def get(self, data: GetShopUiIdSchema):
        return await self.repo.get(data=data)

    async def getby_id(self, id: str, shop_id: str):
        return await self.repo.getby_id(
            id=id,
            shop_id=shop_id,
        )

    async def get_by_entity_type(
        self,
        shop_id: str,
        entity_type: str,
    ):
        return await self.repo.get_by_entity_type(
            shop_id=shop_id,
            entity_type=entity_type,
        )

    async def get_next_number(
        self,
        shop_id: str,
        entity_type: str,
    ):
        """
        Atomically increments current_number and
        returns the updated configuration.
        """
        return await self.repo.get_next_number(
            shop_id=shop_id,
            entity_type=entity_type,
        )