from infras.read_db.main import ACTIVITY_LOGS_COLLECTION
from infras.read_db.models.activity_log_model import ActivityLogReadModel
from schemas.v1.request_schemas.activity_log_schema import ActivityLogSchema
from icecream import ic

class ActivityLogReadDbRepo:
    @classmethod
    async def create_log(cls, data: ActivityLogSchema) -> bool:
        try:
            structured_data = ActivityLogReadModel(**data.model_dump()).model_dump(mode="json")
            res = await ACTIVITY_LOGS_COLLECTION.insert_one(structured_data)
            return bool(res.acknowledged)
        except Exception as e:
            ic(f"Error creating activity log: {e}")
            return False

    @classmethod
    async def get_logs(cls, shop_id: str, limit: int = 50, offset: int = 0) -> list[dict]:
        try:
            cursor = ACTIVITY_LOGS_COLLECTION.find({"shop_id": shop_id}).sort("created_at", -1).skip(offset).limit(limit)
            logs = await cursor.to_list(length=limit)
            # Remove MongoDB's internal _id field
            for log in logs:
                log.pop("_id", None)
            return logs
        except Exception as e:
            ic(f"Error fetching activity logs: {e}")
            return []
