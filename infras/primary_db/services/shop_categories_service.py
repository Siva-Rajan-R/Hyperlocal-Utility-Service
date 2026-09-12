import os
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
from core.constants import DEFAULT_CATEGORIES, SHOP_CATEGORIES_MAPPING
from typing import Optional, List
from icecream import ic

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "http://127.0.0.1:8004/inventories")

class ShopCategoryService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo = ShopCategoryRepo(session=session)
        self.msg_config = RabbitMQMessagingConfig()

    async def _check_if_in_use(self, shop_id: str, category_id: str) -> bool:
        # 1. First check MongoDB directly
        try:
            from infras.read_db.main import MONGO_CLIENT
            inv_coll = MONGO_CLIENT["InventoryServiceReadDb"]["ProdInvCollections"]
            doc = await inv_coll.find_one({
                "shop_id": shop_id,
                "$or": [
                    {"category_id": category_id},
                    {"category_infos.id": category_id}
                ]
            })
            if doc:
                return True
        except Exception as e:
            ic(f"Error checking category usage in Mongo: {e}")

        # 2. Check Inventory Service via HTTP
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                res = await client.get(f"{INVENTORY_SERVICE_URL}/by/shop/{shop_id}?category_id={category_id}&limit=1")
                if res.status_code == 200:
                    data = res.json()
                    products = data.get("data", [])
                    if isinstance(products, list) and len(products) > 0:
                        return True
                    elif isinstance(products, dict):
                        datas = products.get("datas") or []
                        if len(datas) > 0:
                            return True
            except Exception as e:
                ic(f"Error checking category usage in inventory service: {e}")
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



    async def init_categories(self, shop_id: str, categories: Optional[List[str]] = None):
        existing = await self.repo.get(GetShopCategorySchema(shop_id=shop_id, limit=1))
        if existing:
            ic("Categories already initialized for shop", shop_id)
            return True

        target_product_cats = []
        seen_names = set()

        if categories and isinstance(categories, list):
            for shop_cat in categories:
                cat_upper = str(shop_cat).upper().strip()
                mapped_list = None
                for key, val in SHOP_CATEGORIES_MAPPING.items():
                    key_upper = key.upper().strip()
                    if cat_upper == key_upper or cat_upper in key_upper or key_upper in cat_upper:
                        mapped_list = val
                        break
                    key_parts = [p.strip() for p in key_upper.split('/') if p.strip()]
                    cat_parts = [p.strip() for p in cat_upper.split('/') if p.strip()]
                    if any(cp == kp or cp in kp or kp in cp for cp in cat_parts for kp in key_parts):
                        mapped_list = val
                        break
                if not mapped_list:
                    mapped_list = DEFAULT_CATEGORIES
                
                for item in mapped_list:
                    if item['name'] not in seen_names:
                        seen_names.add(item['name'])
                        target_product_cats.append(item)

        if not target_product_cats:
            target_product_cats = DEFAULT_CATEGORIES

        data = []
        for item in target_product_cats:
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

    async def get_predefined_shop_categories(self):
        return SHOP_CATEGORIES_MAPPING

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
        old_cat = await self.repo.getby_id(id=data.id, shop_id=data.shop_id)
        if not old_cat:
            raise ValueError(f"Category with ID '{data.id}' not found.")
        
        is_default = old_cat.get("is_default") if isinstance(old_cat, dict) else getattr(old_cat, "is_default", False)
        if is_default:
            raise ValueError("Default category cannot be deleted.")

        # Check if category is used by any products
        in_use = await self._check_if_in_use(data.shop_id, data.id)
        if in_use:
            category_name = (old_cat.get('name') if isinstance(old_cat, dict) else getattr(old_cat, 'name', None)) or data.id
            raise ValueError(f"Cannot delete category '{category_name}' because products are associated with this category.")

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
