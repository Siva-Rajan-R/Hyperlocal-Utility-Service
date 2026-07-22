from fastapi import APIRouter, Depends, Query, HTTPException
from schemas.v1.request_schemas.activity_log_schema import ActivityLogSchema, GetActivityLogSchema
from infras.read_db.repos.activity_log_repo import ActivityLogReadDbRepo
from typing import Optional

router = APIRouter(
    prefix='/activity-logs',
    tags=['Activity Logs']
)

@router.post('')
async def create_activity_log(data: ActivityLogSchema):
    success = await ActivityLogReadDbRepo.create_log(data=data)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create activity log")
    return {"status_code": 201, "success": True, "msg": "Activity log created successfully"}

@router.get('/{shop_id}')
async def get_activity_logs(shop_id: str, limit: int = 50, offset: int = 0, q: Optional[str] = Query(None), from_date: Optional[str] = Query(None), to_date: Optional[str] = Query(None)):
    logs = await ActivityLogReadDbRepo.get_logs(shop_id=shop_id, limit=limit, offset=offset, query=q, from_date=from_date, to_date=to_date)
    return {
        "detail": {
            "status_code": 200,
            "success": True,
            "msg": "Activity logs fetched successfully"
        },
        "data": logs
    }
