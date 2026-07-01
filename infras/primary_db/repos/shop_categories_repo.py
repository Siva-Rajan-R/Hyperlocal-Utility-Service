from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, or_, and_
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from ..models.shop_categories import ShopCategories
from schemas.v1.db_schemas.shop_category_schema import CreateShopCategoryDbSchema, UpdateShopCategoryDbSchema
from schemas.v1.request_schemas.shop_category_schema import GetShopCategorySchema, DeleteShopCategorySchema
from typing import Optional,List


class ShopCategoryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cols = (
            ShopCategories.id,
            ShopCategories.shop_id,
            ShopCategories.name,
            ShopCategories.description,
            ShopCategories.is_default,
            ShopCategories.is_active,
            ShopCategories.created_at,
            ShopCategories.updated_at
        )

    @start_db_transaction
    async def create(self, data: CreateShopCategoryDbSchema):
        stmt = insert(ShopCategories).values(**data.model_dump(mode="json")).returning(*self.cols)
        res = (await self.session.execute(stmt)).mappings().one_or_none()
        return res

    @start_db_transaction
    async def create_bulk(self, data: List[ShopCategories]):
        self.session.add_all(data)
        return True

    @start_db_transaction
    async def update(self, data: UpdateShopCategoryDbSchema):
        stmt = (
            update(ShopCategories)
            .where(
                and_(
                    ShopCategories.id == data.id,
                    ShopCategories.shop_id == data.shop_id,
                    ShopCategories.is_default == False
                )
            )
            .values(**data.model_dump(mode="json", exclude_none=True, exclude_unset=True))
            .returning(*self.cols)
        )
        return (await self.session.execute(stmt)).mappings().one_or_none()

    @start_db_transaction
    async def delete(self, data: DeleteShopCategorySchema):
        stmt = (
            delete(ShopCategories)
            .where(
                and_(
                    ShopCategories.id == data.id,
                    ShopCategories.shop_id == data.shop_id,
                    ShopCategories.is_default == False
                )
            )
            .returning(*self.cols)
        )
        return (await self.session.execute(stmt)).mappings().one_or_none()

    async def get(self, data: GetShopCategorySchema):
        cursor = (data.offset - 1) * data.limit
        stmt = (
            select(*self.cols)
            .where(
                and_(
                    or_(
                        ShopCategories.shop_id == data.shop_id,
                        ShopCategories.shop_id == "DEFAULT"
                    ),
                    ShopCategories.is_active == True
                )
            )
            .offset(cursor)
            .limit(data.limit)
            .order_by(ShopCategories.is_default.desc(), ShopCategories.name.asc())
        )
        return (await self.session.execute(stmt)).mappings().all()

    async def getby_id(self, id: str, shop_id: str):
        stmt = (
            select(*self.cols)
            .where(
                and_(
                    ShopCategories.id == id,
                    or_(
                        ShopCategories.shop_id == shop_id,
                        ShopCategories.shop_id == "DEFAULT"
                    )
                )
            )
        )
        return (await self.session.execute(stmt)).mappings().one_or_none()
