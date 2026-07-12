import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from models.service_models.base_service_model import BaseServiceModel
from schemas.v1.request_schemas.shop_unit_schema import CreateShopUnitSchema, UpdateShopUnitSchema, DeleteShopUnitSchema, GetShopUnitSchema
from schemas.v1.db_schemas.shop_unit_schema import CreateShopUnitDbSchema, UpdateShopUnitDbSchema
from ..repos.shop_units_repo import ShopUnitRepo
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from messaging.main import RabbitMQMessagingConfig
from datetime import datetime, timezone
from ..models.shop_units import ShopUnits
from typing import Optional,List
from core.constants import DEFAULT_UNITS
from icecream import ic

INVENTORY_SERVICE_URL = "http://127.0.0.1:8000/inventories"

class ShopUnitService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo = ShopUnitRepo(session=session)
        self.msg_config = RabbitMQMessagingConfig()

    async def _check_if_in_use(self, shop_id: str, unit_id: str) -> bool:
        offset = 1
        limit = 100
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    res = await client.get(f"{INVENTORY_SERVICE_URL}/by/shop/{shop_id}?limit={limit}&offset={offset}")
                    if res.status_code == 200:
                        data = res.json()
                        products = data.get("data", [])
                        if not products:
                            break
                        
                        for p in products:
                            if p.get("unit_id") == unit_id:
                                return True
                        
                        if len(products) < limit:
                            break
                        offset += 1
                    else:
                        break
                except Exception:
                    break
        return False

    async def _emit_event(self, action: str, unit_id: str, shop_id: str):
        payload = {
            "entity": "ShopUnit",
            "action": action,
            "id": unit_id,
            "shop_id": shop_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        headers = {
            "routing_key": f"utility.shop_unit.{action.lower()}",
            "exchange_name": "utility_exchange",
            "entity_name": "shop_unit",
            "service_name": "UTILITY",
            "saga_id": "none",
            "reply_key": "none",
            "reply_exchange": "none",
            "reply_entity_name": "none",
            "body": payload
        }
        await self.msg_config.publish_event(
            routing_key=headers["routing_key"],
            exchange_name=headers["exchange_name"],
            payload=payload,
            headers=headers
        )

    async def init_units(self, shop_id: str):
        existing = await self.repo.get(GetShopUnitSchema(shop_id=shop_id, limit=1))
        if existing:
            ic("Units already initialized for shop", shop_id)
            return True

        data = []
        for item in DEFAULT_UNITS:
            data.append(
                ShopUnits(
                    id=generate_uuid(),
                    shop_id=shop_id,
                    name=item['name'],
                    short_name=item['short_name'],
                    description=item["description"],
                    is_default=True,
                    is_active=True,
                    sub_units=item.get("sub_units", []),
                )

            )

        res = await self.repo.create_bulk(data=data)
        ic(res)
        return res

    async def create(self, data: CreateShopUnitSchema):
        existing = await self.repo.get_by_name(shop_id=data.shop_id, name=data.name)
        if existing:
            ic(f"A unit with the name '{data.name}' already exists.")
            return False

        unit_id = generate_uuid()
        db_data = CreateShopUnitDbSchema(
            id=unit_id,
            **data.model_dump()
        )
        res = await self.repo.create(data=db_data)
        # if res:
        #     await self._emit_event("CREATED", unit_id, data.shop_id)
            
        #     unit_name = data.name if hasattr(data, 'name') else 'Unknown'
        #     await ActivityLogger.log(
        #         shop_id=data.shop_id,
        #         service="Utility",
        #         action="CREATE",
        #         entity_type="ShopUnit",
        #         entity_id=unit_id,
        #         description=f"Created shop unit: {unit_name}",
        #         changes=[{"field": "name", "before": "", "after": str(unit_name)}]
        #     )
        return res

    async def update(self, data: UpdateShopUnitSchema):
        old_unit = await self.repo.getby_id(id=data.id, shop_id=data.shop_id)
        if not old_unit:
            raise Exception("Unit not found")

        # Duplicate check if name is being updated
        if data.name and data.name.lower() != (old_unit.get("name") or old_unit.name).lower():
            existing = await self.repo.get_by_name(shop_id=data.shop_id, name=data.name)
            if existing and existing.id != data.id:
                raise ValueError(f"A unit with the name '{data.name}' already exists.")
        
        if data.sub_units:
            base_name = data.name or old_unit.get("name") or old_unit.name
            base_name_lower = base_name.lower()
            seen_names = set()
            seen_factors = set()
            for su in data.sub_units:
                su_name_lower = su.name.lower()
                if su_name_lower == base_name_lower:
                    raise ValueError(f"Base unit '{base_name}' cannot be added as a sub unit")
                if su_name_lower in seen_names:
                    raise ValueError(f"Duplicate sub unit name: {su.name}")
                if su.factor in seen_factors:
                    raise ValueError(f"Duplicate conversion factor: {su.factor}")
                seen_names.add(su_name_lower)
                seen_factors.add(su.factor)

        res = await self.repo.update(data=UpdateShopUnitDbSchema(**data.model_dump(exclude_unset=True)))
        # if res and old_unit:
        #     await self._emit_event("UPDATED", data.id, data.shop_id)
            
        #     changes_list = ActivityLogger.compute_changes(old_unit, data.model_dump(exclude_none=True, exclude_unset=True))
        #     if changes_list:
        #         desc_changes = [f"{c['field']} prv({c['before']}) after ({c['after']})" for c in changes_list]
        #         desc = f"updated shop unit {', '.join(desc_changes)}"
        #         await ActivityLogger.log(
        #             shop_id=data.shop_id,
        #             service="Utility",
        #             action="UPDATE",
        #             entity_type="ShopUnit",
        #             entity_id=data.id,
        #             description=desc,
        #             changes=changes_list
        #         )
        return res

    async def delete(self, data: DeleteShopUnitSchema):
        in_use = await self._check_if_in_use(data.shop_id, data.id)
        if in_use:
            raise Exception("Unit is currently in use by products and cannot be deleted.")

        old_unit = await self.repo.getby_id(id=data.id, shop_id=data.shop_id)
        res = await self.repo.delete(data=data)
        if res:
            await self._emit_event("DELETED", data.id, data.shop_id)
            
            unit_name = old_unit.get('name', 'Unknown') if old_unit else 'Unknown'
            await ActivityLogger.log(
                shop_id=data.shop_id,
                service="Utility",
                action="DELETE",
                entity_type="ShopUnit",
                entity_id=data.id,
                description=f"Deleted shop unit: {unit_name}",
                changes=[{"field": "name", "before": str(unit_name), "after": "DELETED"}]
            )
        return res

    async def get(self, data: GetShopUnitSchema):
        return await self.repo.get(data=data)

    async def getby_id(self, id: str, shop_id: str):
        return await self.repo.getby_id(id=id, shop_id=shop_id)
