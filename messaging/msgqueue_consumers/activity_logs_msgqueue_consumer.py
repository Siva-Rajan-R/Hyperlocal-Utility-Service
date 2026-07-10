from aio_pika.abc import AbstractIncomingMessage
import orjson
from icecream import ic
from schemas.v1.request_schemas.activity_log_schema import ActivityLogSchema
from infras.read_db.repos.activity_log_repo import ActivityLogReadDbRepo
from infras.primary_db.main import AsyncUtilisLocalSession
from infras.primary_db.services.shop_categories_service import ShopCategoryService
from infras.primary_db.services.shop_units_service import ShopUnitService
from infras.primary_db.services.shop_ui_id_service import ShopUiIdService

async def init_defaults(shop_id: str):
    async with AsyncUtilisLocalSession() as session:
        try:
            ic(f"Initializing defaults for shop {shop_id}...")
            # 1. Initialize Categories
            await ShopCategoryService(session=session).init_categories(shop_id=shop_id)
            # 2. Initialize Units
            await ShopUnitService(session=session).init_units(shop_id=shop_id)
            # 3. Initialize UI IDs
            await ShopUiIdService(session=session).init_ids(shop_id=shop_id)
            await session.commit()
            ic(f"Defaults successfully initialized for shop {shop_id}")
        except Exception as err:
            ic(f"Failed to initialize defaults for shop {shop_id}: {err}")
            await session.rollback()

async def activity_logs_consumer_handler(msg: AbstractIncomingMessage):
    async with msg.process(requeue=True):
        try:
            payload = orjson.loads(msg.body)
            # Create ActivityLogSchema from payload
            data = ActivityLogSchema(**payload)
            
            success = await ActivityLogReadDbRepo.create_log(data=data)
            if success:
                ic(f"Successfully processed activity log for {data.entity_type} ID: {data.entity_id}")
                if data.entity_type == "Shop" and data.action == "CREATE":
                    await init_defaults(data.shop_id)
            else:
                ic(f"Failed to process activity log for {data.entity_type} ID: {data.entity_id}")
                # We could potentially raise here if we want to requeue on DB error
        except Exception as e:
            ic(f"Error processing activity log message: {e}")
            # The msg.process() context manager handles nacking/requeueing if an exception is raised
            raise e
