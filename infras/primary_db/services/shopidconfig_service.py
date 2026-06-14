from sqlalchemy.ext.asyncio import AsyncSession

from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from ..repos.shopidconfig_repo import ShopIdConfigRepo


# Default config applied when no shop config exists yet
DEFAULT_CONFIG = {
    "purchase":        {"prefix": "PUR", "start_from": 1},
    "stock_movement":  {"prefix": "SMV", "start_from": 1},
    "inventory":       {"prefix": "INV", "start_from": 1},
    "customer":        {"prefix": "CUS", "start_from": 1},
    "supplier":        {"prefix": "SUP", "start_from": 1},
    "employee":        {"prefix": "EMP", "start_from": 1},
    "order":           {"prefix": "ORD", "start_from": 1},
    "billing":         {"prefix": "BIL", "start_from": 1},
}


class ShopIdConfigService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, shop_id: str):
        row = await ShopIdConfigRepo(session=self.session).get_by_shop(shop_id=shop_id)
        if row:
            return dict(row)
        # Return defaults with a generated id (not yet persisted)
        return {
            "id": None,
            "shop_id": shop_id,
            "config": DEFAULT_CONFIG,
        }

    async def upsert(self, shop_id: str, config: dict):
        existing = await ShopIdConfigRepo(session=self.session).get_by_shop(shop_id=shop_id)
        row_id = existing["id"] if existing else generate_uuid()
        return await ShopIdConfigRepo(session=self.session).upsert(
            id=row_id, shop_id=shop_id, config=config
        )
