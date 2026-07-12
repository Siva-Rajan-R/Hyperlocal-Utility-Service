from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, or_, and_,func
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from ..models.shop_units import ShopUnits
from schemas.v1.db_schemas.shop_unit_schema import CreateShopUnitDbSchema, UpdateShopUnitDbSchema
from schemas.v1.request_schemas.shop_unit_schema import GetShopUnitSchema, DeleteShopUnitSchema
from typing import Optional,List

class ShopUnitRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cols = (
            ShopUnits.id,
            ShopUnits.shop_id,
            ShopUnits.name,
            ShopUnits.short_name,
            ShopUnits.description,
            ShopUnits.is_default,
            ShopUnits.is_active,
            ShopUnits.sub_units,
            ShopUnits.created_at,
            ShopUnits.updated_at
        )

    @start_db_transaction
    async def create(self, data: CreateShopUnitDbSchema):
        stmt = insert(ShopUnits).values(**data.model_dump(mode="json")).returning(*self.cols)
        res = (await self.session.execute(stmt)).mappings().one_or_none()
        return res

    @start_db_transaction
    async def create_bulk(self, data: List[ShopUnits]):
        self.session.add_all(data)
        return True
    
    @start_db_transaction
    async def update(self, data: UpdateShopUnitDbSchema):
        stmt = (
            update(ShopUnits)
            .where(
                and_(
                    ShopUnits.id == data.id,
                    ShopUnits.shop_id == data.shop_id,
                    ShopUnits.is_default == False
                )
            )
            .values(**data.model_dump(mode="json", exclude_none=True, exclude_unset=True))
            .returning(*self.cols)
        )
        return (await self.session.execute(stmt)).mappings().one_or_none()

    @start_db_transaction
    async def delete(self, data: DeleteShopUnitSchema):
        stmt = (
            delete(ShopUnits)
            .where(
                and_(
                    ShopUnits.id == data.id,
                    ShopUnits.shop_id == data.shop_id,
                    ShopUnits.is_default == False
                )
            )
            .returning(*self.cols)
        )
        return (await self.session.execute(stmt)).mappings().one_or_none()

    async def get(self, data: GetShopUnitSchema):
        cursor = (data.offset - 1) * data.limit
        is_active_val = data.is_active if data.is_active is not None else True
        stmt = (
            select(*self.cols)
            .where(
                and_(
                    or_(
                        ShopUnits.shop_id == data.shop_id,
                        ShopUnits.shop_id == "DEFAULT"
                    ),
                    ShopUnits.is_active == is_active_val
                )
            )
            .offset(cursor)
            .limit(data.limit)
            .order_by(ShopUnits.is_default.desc(), ShopUnits.name.asc())
        )
        return (await self.session.execute(stmt)).mappings().all()

    async def getby_id(self, id: str, shop_id: str):
        stmt = (
            select(*self.cols)
            .where(
                and_(
                    ShopUnits.id == id,
                    or_(
                        ShopUnits.shop_id == shop_id,
                        ShopUnits.shop_id == "DEFAULT"
                    )
                )
            )
        )
        return (await self.session.execute(stmt)).mappings().one_or_none()

    async def get_by_name(self, shop_id: str, name: str):
        stmt = (
            select(*self.cols)
            .where(
                and_(
                    ShopUnits.shop_id == shop_id,
                    func.lower(ShopUnits.name) == name.lower()
                )
            )
        )
        return (await self.session.execute(stmt)).mappings().one_or_none()
