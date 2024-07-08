from fastapi import APIRouter, Request, Depends, Form, HTTPException
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
    if not await redis_services.new_metadata(
        file_data=file_data, redis_connection=redis_connection
    ):
        raise HTTPException(status_code=500, detail="Not stored in database")
    return {
        "message": "Metadata Stored",
        "storage_info": f"FileData{file_data.file_id}",
    }


@router.get("/getMetadata")
async def get_file_metadata(
    file_id: Annotated[UUID, Form()],
    redis_connection: redis.Redis = Depends(dependency.get_redis),
):
    metadata = await redis_services.get_metadata(
        file_id=file_id, redis_connection=redis_connection
    )
    return metadata
