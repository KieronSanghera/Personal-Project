import redis.asyncio as redis
from uuid import UUID
import json
from app.schemas.schemas import FileInformation
from app.exceptions.redis_exceptions import RedisException
from pydantic import ValidationError
import logging


async def new_metadata(file_data: FileInformation, redis_connection: redis.Redis):
    response = await redis_connection.hset(
        name=f"FileData{file_data.file_id}",
        key="metadata",
        value=str(file_data.model_dump_database()),
    )
    if response < 1:
        exists = await redis_connection.exists(f"FileData{file_data.file_id}")
        if not exists:
            return False

    return True


async def get_metadata(file_id: UUID, redis_connection: redis.Redis):
    
    metadata_bytes: bytes = await redis_connection.hget(
        f"FileData{file_id}", key="metadata"
    )
    
    if not isinstance(metadata_bytes, bytes):
        redis_exception = await RedisException.redis_check(f"Retrieved none Byte type for redis hget. Retrieved type - {type(metadata_bytes)} - Contents - ")
        raise redis_exception
    
    decoded_metadata: str = metadata_bytes.decode().replace("'", '"')
    metadata = json.loads(decoded_metadata)
    try:
        file_info = FileInformation(**metadata)
    except ValidationError as error:
        logging.error(f"Malformed dict for FileInformation schema type - error - {error} - dict - {metadata}")
        raise 
    return file_info

async def delete_metadata(file_id: UUID, redis_connection: redis.Redis):
    data_keys = await redis_connection.hkeys(name=f"FileData{file_id}")
    response = await redis_connection.hdel(f"FileData{file_id}", *data_keys)
    if response < 1:
        exists = await redis_connection.exists(f"FileData{file_id}")
        if exists:
            return False

    return True
