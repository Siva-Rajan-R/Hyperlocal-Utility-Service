import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from models.service_models.base_service_model import BaseServiceModel
from schemas.v1.request_schemas.shop_category_schema import CreateShopCategorySchema, UpdateShopCategorySchema, DeleteShopCategorySchema, GetShopCategorySchema
from schemas.v1.db_schemas.shop_category_schema import CreateShopCategoryDbSchema, UpdateShopCategoryDbSchema
from ..repos.shop_categories_repo import ShopCategoryRepo
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from messaging.main import RabbitMQMessagingConfig
from datetime import datetime, timezone
from ..models.shop_categories import ShopCategories
from core.constants import DEFAULT_CATEGORIES
from icecream import ic

INVENTORY_SERVICE_URL = "http://127.0.0.1:8000/inventories"

class ShopCategoryService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo = ShopCategoryRepo(session=session)
        self.msg_config = RabbitMQMessagingConfig()

    async def _check_if_in_use(self, shop_id: str, category_id: str) -> bool:
        # Check if any products use this category in Inventory Service
        offset = 1
        limit = 100
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    # using the schema GetProductsByShopId format
                    res = await client.get(f"{INVENTORY_SERVICE_URL}/by/shop/{shop_id}?limit={limit}&offset={offset}")
                    if res.status_code == 200:
                        data = res.json()
                        products = data.get("data", [])
                        if not products:
                            break
                        
                        for p in products:
                            if p.get("category_id") == category_id:
                                return True
                        
                        if len(products) < limit:
                            break
                        offset += 1
                    else:
                        break
                except Exception:
                    break
        return False

    async def _emit_event(self, action: str, category_id: str, shop_id: str):
        payload = {
            "entity": "ShopCategory",
            "action": action,
            "id": category_id,
            "shop_id": shop_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        headers = {
            "routing_key": f"utility.shop_category.{action.lower()}",
            "exchange_name": "utility_exchange",
            "entity_name": "shop_category",
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



    async def init_categories(self, shop_id: str):
        existing = await self.repo.get(GetShopCategorySchema(shop_id=shop_id, limit=1))
        if existing:
            ic("Categories already initialized for shop", shop_id)
            return True

        data = []
        for item in DEFAULT_CATEGORIES:
            data.append(
                ShopCategories(
                    id=generate_uuid(),
                    shop_id=shop_id,
                    name=item['name'],
                    description=item["description"],
                    is_default=True,
                    is_active=True,
                )

            )

        res = await self.repo.create_bulk(data=data)
        ic(res)
        return res

    async def create(self, data: CreateShopCategorySchema):
        existing = await self.repo.get_by_name(shop_id=data.shop_id, name=data.name)
        if existing:
            ic(f"A category with the name '{data.name}' already exists.")
            return False

        cat_id = generate_uuid()
        db_data = CreateShopCategoryDbSchema(
            id=cat_id,
            **data.model_dump()
        )
        res = await self.repo.create(data=db_data)
        # if res:
        #     await self._emit_event("CREATED", cat_id, data.shop_id)
            
        #     category_name = data.name if hasattr(data, 'name') else 'Unknown'
        #     await ActivityLogger.log(
        #         shop_id=data.shop_id,
        #         service="Utility",
        #         action="CREATE",
        #         entity_type="ShopCategory",
        #         entity_id=cat_id,
        #         description=f"Created shop category: {category_name}",
        #         changes=[{"field": "name", "before": "", "after": str(category_name)}]
        #     )
        return res

    async def update(self, data: UpdateShopCategorySchema):
        # We don't check if it's default here, because repo update handles `is_default == False`
        old_cat = await self.repo.getby_id(id=data.id, shop_id=data.shop_id)
        if not old_cat:
            raise Exception("Category not found")

        # Duplicate check if name is being updated
        if data.name and data.name.lower() != (old_cat.get("name") or old_cat.name).lower():
            existing = await self.repo.get_by_name(shop_id=data.shop_id, name=data.name)
            if existing and existing.id != data.id:
                raise ValueError(f"A category with the name '{data.name}' already exists.")

        res = await self.repo.update(data=UpdateShopCategoryDbSchema(**data.model_dump(exclude_unset=True)))
        # if res and old_cat:
        #     await self._emit_event("UPDATED", data.id, data.shop_id)
            
        #     changes_list = ActivityLogger.compute_changes(old_cat, data.model_dump(exclude_none=True, exclude_unset=True))
        #     if changes_list:
        #         desc_changes = [f"{c['field']} prv({c['before']}) after ({c['after']})" for c in changes_list]
        #         desc = f"updated shop category {', '.join(desc_changes)}"
        #         await ActivityLogger.log(
        #             shop_id=data.shop_id,
        #             service="Utility",
        #             action="UPDATE",
        #             entity_type="ShopCategory",
        #             entity_id=data.id,
        #             description=desc,
        #             changes=changes_list
        #         )
        return res

    async def delete(self, data: DeleteShopCategorySchema):
        # Check if category is used
        in_use = await self._check_if_in_use(data.shop_id, data.id)
        if in_use:
            raise Exception("Category is currently in use by products and cannot be deleted.")

        old_cat = await self.repo.getby_id(id=data.id, shop_id=data.shop_id)
        res = await self.repo.delete(data=data)
        if res:
            await self._emit_event("DELETED", data.id, data.shop_id)
            
            category_name = old_cat.get('name', 'Unknown') if old_cat else 'Unknown'
            await ActivityLogger.log(
                shop_id=data.shop_id,
                service="Utility",
                action="DELETE",
                entity_type="ShopCategory",
                entity_id=data.id,
                description=f"Deleted shop category: {category_name}",
                changes=[{"field": "name", "before": str(category_name), "after": "DELETED"}]
            )
        return res

    async def get(self, data: GetShopCategorySchema):
        return await self.repo.get(data=data)

    async def getby_id(self, id: str, shop_id: str):
        return await self.repo.getby_id(id=id, shop_id=shop_id)
