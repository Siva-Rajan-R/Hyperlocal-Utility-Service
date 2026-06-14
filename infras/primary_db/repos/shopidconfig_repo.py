from ..models.shop_id_config import ShopIdConfig
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction


class ShopIdConfigRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    @start_db_transaction
    async def upsert(self, id: str, shop_id: str, config: dict):
        """Insert or replace the full config for a shop."""
        existing = await self.session.get(ShopIdConfig, id)
        if existing:
            existing.config = config
        else:
            self.session.add(ShopIdConfig(id=id, shop_id=shop_id, config=config))
        return True

    async def get_by_shop(self, shop_id: str):
        stmt = select(
            ShopIdConfig.id,
            ShopIdConfig.shop_id,
            ShopIdConfig.config,
        ).where(ShopIdConfig.shop_id == shop_id)
        row = (await self.session.execute(stmt)).mappings().one_or_none()
        return row
