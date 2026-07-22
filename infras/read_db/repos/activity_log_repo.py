from infras.read_db.main import ACTIVITY_LOGS_COLLECTION
from infras.read_db.models.activity_log_model import ActivityLogReadModel
from schemas.v1.request_schemas.activity_log_schema import ActivityLogSchema
from icecream import ic
from typing import Optional

def _is_empty_or_none(val) -> bool:
    if val is None:
        return True
    if isinstance(val, (dict, list, set, str, tuple)) and len(val) == 0:
        return True
    val_str = str(val).strip()
    if val_str in ("None", "{}", "[]", "", "null", "NoneType"):
        return True
    return False

class ActivityLogReadDbRepo:
    @classmethod
    async def create_log(cls, data: ActivityLogSchema) -> bool:
        try:
            structured_data = ActivityLogReadModel(**data.model_dump()).model_dump(mode="json")
            if structured_data.get("changes"):
                cleaned_changes = []
                for c in structured_data["changes"]:
                    b_val = c.get("before")
                    a_val = c.get("after")
                    if _is_empty_or_none(b_val) and _is_empty_or_none(a_val):
                        continue
                    if str(b_val).strip() == str(a_val).strip():
                        continue
                    cleaned_changes.append(c)
                structured_data["changes"] = cleaned_changes
            res = await ACTIVITY_LOGS_COLLECTION.insert_one(structured_data)
            return bool(res.acknowledged)
        except Exception as e:
            ic(f"Error creating activity log: {e}")
            return False

    @classmethod
    async def get_logs(cls, shop_id: str, limit: int = 50, offset: int = 0, query: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None) -> list[dict]:
        try:
            from datetime import datetime
            search_filter = {"shop_id": shop_id}
            if query:
                search_filter["$or"] = [
                    {"entity_id": {"$regex": query, "$options": "i"}},
                    {"entity_name": {"$regex": query, "$options": "i"}},
                    {"user_name": {"$regex": query, "$options": "i"}},
                    {"service": {"$regex": query, "$options": "i"}},
                    {"entity_type": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}}
                ]
            if from_date:
                try:
                    from_dt = datetime.strptime(from_date, "%Y-%m-%d").isoformat()
                    if "created_at" not in search_filter: search_filter["created_at"] = {}
                    search_filter["created_at"]["$gte"] = from_dt
                except Exception:
                    pass
            if to_date:
                try:
                    to_date_str = to_date
                    if len(to_date_str) <= 10: to_date_str += ' 23:59:59'
                    to_dt = datetime.strptime(to_date_str, "%Y-%m-%d %H:%M:%S").isoformat()
                    if "created_at" not in search_filter: search_filter["created_at"] = {}
                    search_filter["created_at"]["$lte"] = to_dt
                except Exception:
                    pass

            cursor = ACTIVITY_LOGS_COLLECTION.find(search_filter).sort("created_at", -1).skip(offset).limit(limit)
            logs = await cursor.to_list(length=limit)
            for log in logs:
                log.pop("_id", None)
            return logs
        except Exception as e:
            ic(f"Error fetching activity logs: {e}")
            return []
