import redis.asyncio as redis
from uuid import UUID
import json
from app.schemas.schemas import FileInformation


async def get_metadata(file_id: UUID, redis_connection: redis.Redis):
    metadata_bytes: bytes = await redis_connection.hget(
        f"FileData{file_id}", key="metadata"
    )
    decoded_metadata: str = metadata_bytes.decode().replace("'", '"')
    metadata = json.loads(decoded_metadata)

    file_info = FileInformation(**metadata)

    return file_info
