from fastapi import APIRouter, Request, Depends, Form
from typing import Annotated
import redis.asyncio as redis
from app.dependencies import dependency
from app.schemas.schemas import FileInformation
from app.services import redis_services
from uuid import UUID
import json


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Default"}


@router.post("/newMetadata")
async def new_metadata(
    file_data: FileInformation = Depends(FileInformation.as_form),
    redis_connection: redis.Redis = Depends(dependency.get_redis),
):
    await redis_connection.hset(name=f"FileData{file_data.file_id}", key="metadata", value=str(file_data.model_dump()))
    print(file_data.model_dump_database())
    
    return {"message": "Metadata Stored", "storage_info": f"FileData{file_data.file_id}"}
    
@router.get("/getMetadata")
async def get_file_metadata(
    file_id: Annotated[UUID, Form()],
    redis_connection: redis.Redis = Depends(dependency.get_redis),
):
    metadata = await redis_services.get_metadata(file_id=file_id, redis_connection=redis_connection)    
    print(metadata)
    return metadata
    



### TODO: redis connection now set, need to probably use hash (learn
#   about it more first). Then need to structure request by getting
#   the information to store and then storing that for the first time.
#
#   What I might need, file information and everything else too?
#   Separate ones for each or all together
###
