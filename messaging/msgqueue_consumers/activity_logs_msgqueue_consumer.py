from aio_pika.abc import AbstractIncomingMessage
import orjson
from icecream import ic
from schemas.v1.request_schemas.activity_log_schema import ActivityLogSchema
from infras.read_db.repos.activity_log_repo import ActivityLogReadDbRepo

async def activity_logs_consumer_handler(msg: AbstractIncomingMessage):
    async with msg.process(requeue=True):
        try:
            payload = orjson.loads(msg.body)
            # Create ActivityLogSchema from payload
            data = ActivityLogSchema(**payload)
            
            success = await ActivityLogReadDbRepo.create_log(data=data)
            if success:
                ic(f"Successfully processed activity log for {data.entity_type} ID: {data.entity_id}")
            else:
                ic(f"Failed to process activity log for {data.entity_type} ID: {data.entity_id}")
                # We could potentially raise here if we want to requeue on DB error
        except Exception as e:
            ic(f"Error processing activity log message: {e}")
            # The msg.process() context manager handles nacking/requeueing if an exception is raised
            raise e
