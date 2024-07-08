import redis.asyncio as redis
from uuid import UUID
import json
from app.schemas.schemas import FileInformation


async def new_metadata(file_data: FileInformation, redis_connection: redis.Redis):
    
    response = await redis_connection.hset(name=f"FileData{file_data.file_id}", key="metadata", value=str(file_data.model_dump_database()))
    # check if key exists already
    return response


async def get_metadata(file_id: UUID, redis_connection: redis.Redis):
    metadata_bytes: bytes = await redis_connection.hget(
        f"FileData{file_id}", key="metadata"
    )
    decoded_metadata: str = metadata_bytes.decode().replace("'", '"')
    metadata = json.loads(decoded_metadata)

    file_info = FileInformation(**metadata)

    return file_info
