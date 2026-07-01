from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, and_
from typing import List

from hyperlocal_platform.core.decorators.db_session_handler_dec import (
    start_db_transaction,
)

from ..models.shop_ui_id import ShopUiId

from schemas.v1.db_schemas.shop_ui_id_schema import (
    CreateShopUiIdDbSchema,
    UpdateShopUiIdDbSchema,
)
from schemas.v1.request_schemas.shop_ui_id_schema import (
    GetShopUiIdSchema,
    DeleteShopUiIdSchema,
)


class ShopUiIdRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.cols = (
            ShopUiId.id,
            ShopUiId.shop_id,
            ShopUiId.entity_type,
            ShopUiId.prefix,
            ShopUiId.start_from,
            ShopUiId.current_number,
            ShopUiId.created_at,
            ShopUiId.updated_at,
        )

    @start_db_transaction
    async def create(self, data: CreateShopUiIdDbSchema):
        stmt = (
            insert(ShopUiId)
            .values(**data.model_dump(mode="json"))
            .returning(*self.cols)
        )

        return (
            await self.session.execute(stmt)
        ).mappings().one_or_none()
    

    @start_db_transaction
    async def create_bulk(self, data: List[ShopUiId]):
        self.session.add_all(data)
        return True

    @start_db_transaction
    async def update(self, data: UpdateShopUiIdDbSchema):
        stmt = (
            update(ShopUiId)
            .where(
                and_(
                    ShopUiId.id == data.id,
                    ShopUiId.shop_id == data.shop_id,
                )
            )
            .values(
                **data.model_dump(
                    mode="json",
                    exclude_none=True,
                    exclude_unset=True,
                )
            )
            .returning(*self.cols)
        )

        return (
            await self.session.execute(stmt)
        ).mappings().one_or_none()

    @start_db_transaction
    async def delete(self, data: DeleteShopUiIdSchema):
        stmt = (
            delete(ShopUiId)
            .where(
                and_(
                    ShopUiId.id == data.id,
                    ShopUiId.shop_id == data.shop_id,
                )
            )
            .returning(*self.cols)
        )

        return (
            await self.session.execute(stmt)
        ).mappings().one_or_none()

    async def get(self, data: GetShopUiIdSchema):
        cursor = (data.offset - 1) * data.limit

        stmt = (
            select(*self.cols)
            .where(
                ShopUiId.shop_id == data.shop_id
            )
            .order_by(ShopUiId.entity_type.asc())
            .offset(cursor)
            .limit(data.limit)
        )

        return (
            await self.session.execute(stmt)
        ).mappings().all()

    async def getby_id(self, id: str, shop_id: str):
        stmt = (
            select(*self.cols)
            .where(
                and_(
                    ShopUiId.id == id,
                    ShopUiId.shop_id == shop_id,
                )
            )
        )

        return (
            await self.session.execute(stmt)
        ).mappings().one_or_none()

    async def get_by_entity_type(self, shop_id: str, entity_type: str):
        stmt = (
            select(*self.cols)
            .where(
                and_(
                    ShopUiId.shop_id == shop_id,
                    ShopUiId.entity_type == entity_type,
                )
            )
        )

        return (
            await self.session.execute(stmt)
        ).mappings().one_or_none()

    @start_db_transaction
    async def get_next_number(
        self,
        shop_id: str,
        entity_type: str,
    ):
        stmt = (
            update(ShopUiId)
            .where(
                and_(
                    ShopUiId.shop_id == shop_id,
                    ShopUiId.entity_type == entity_type,
                )
            )
            .values(
                current_number=ShopUiId.current_number + 1
            )
            .returning(*self.cols)
        )

        return (
            await self.session.execute(stmt)
        ).mappings().one_or_none()