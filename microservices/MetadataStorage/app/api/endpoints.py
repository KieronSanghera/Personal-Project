from fastapi import APIRouter, Depends, Form, HTTPException, Request
from typing import Annotated
import redis.asyncio as redis
import redis.exceptions as redis_exception
from app.dependencies import dependency
from app.schemas.schemas import (
    FileInformation,
    CommonEventFormat,
    ConnectionInformation,
    Response,
)
from app.services import redis_service, connection_service
from uuid import UUID
import json
import logging
from app.exceptions.redis_exceptions import RedisException
from pydantic import ValidationError
import asyncio


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Default"}


@router.post("/newMetadata", status_code=201)
async def new_metadata(
    request: Request,
    file_data: FileInformation = Depends(FileInformation.as_form),
    redis_connection: redis.Redis = Depends(dependency.get_redis),
):
    log: CommonEventFormat = CommonEventFormat(version="0.1.0")
    connection_info: ConnectionInformation = connection_service.connection_info(
        request=request
    )

    log.connection_id = connection_info.connection_id
    log.extension["src"] = connection_info.source_addr
    log.extension["host"] = connection_info.host_addr

    log.file_id = file_data.file_id

    try:
        metadata_stored = await redis_service.new_metadata(
            file_data=file_data, redis_connection=redis_connection
        )
    except (
        redis_exception.ConnectionError,
        redis_exception.TimeoutError,
        redis_exception.AuthenticationError,
        redis_exception.ResponseError,
        redis_exception.DataError,
        redis_exception.InvalidResponse,
    ) as error:
        logging.error(f"Connection Error to redis {error}")
        log.event = "New Metadata Storage Request Failed"
        log.severity = 10
        log.log_id = "L0021"
        log.extension["message"] = "New metadata storage request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Redis Error"})
    except asyncio.CancelledError as error:
        logging.error(f"Asyncio error {error}")
        log.event = "New Metadata Storage Request Failed"
        log.severity = 10
        log.log_id = "L0021"
        log.extension["message"] = "New metadata storage request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Asyncio Error"})
    except Exception as error:
        logging.error(f"Unhandled Error raised {error}")
        log.event = "New Metadata Storage Request Failed"
        log.severity = 10
        log.log_id = "L0021"
        log.extension["message"] = "New metadata storage request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Internal Error"})

    if not metadata_stored:
        logging.info(f"Metadata NOT Stored")
        log.event = "New Metadata Storage Request Failed"
        log.severity = 10
        log.log_id = "L0021"
        log.extension["message"] = "New metadata storage request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Metadata NOT Stored"})

    logging.debug("Store Metadata was successful")
    log.event = "Metadata Storage Success"
    log.severity = 5
    log.log_id = "L0020"
    log.extension["message"] = "File Metadata was successfully stored"
    log.log()

    return {
        "message": "Metadata Stored",
        "storage_info": f"FileData{file_data.file_id}",
    }


@router.get("/getMetadata/{file_id}")
async def get_file_metadata(
    request: Request,
    file_id: UUID,
    redis_connection: redis.Redis = Depends(dependency.get_redis),
):
    log: CommonEventFormat = CommonEventFormat(version="0.1.0")
    connection_info: ConnectionInformation = connection_service.connection_info(
        request=request
    )

    log.connection_id = connection_info.connection_id
    log.extension["src"] = connection_info.source_addr
    log.extension["host"] = connection_info.host_addr

    log.file_id = file_id

    try:
        metadata = await redis_service.get_metadata(
            file_id=file_id, redis_connection=redis_connection
        )
    except UnicodeDecodeError as error:
        logging.error(f"Redis bytes decode failed - error - {error}")
        log.event = "Get Metadata Request Failed"
        log.severity = 10
        log.log_id = "L0024"
        log.extension["message"] = "Request to get metadata failed"
        log.log()
        raise HTTPException(500, detail={"message": "Redis Decode Error"})
    except json.JSONDecodeError as error:
        logging.error(f"Retrieved non dict/json object from decoded redis hget {error}")
        log.event = "Get Metadata Request Failed"
        log.severity = 10
        log.log_id = "L0024"
        log.extension["message"] = "Request to get metadata failed"
        log.log()
        raise HTTPException(500, detail={"message": "Redis/Metadata Error"})
    except RedisException as error:
        logging.error(
            f"Tried to retrieve metadata for file -  FileData{file_id} - Error was {error}"
        )
        log.event = "Get Metadata Request Failed"
        log.severity = 10
        log.log_id = "L0024"
        log.extension["message"] = "Request to get metadata failed"
        log.log()
        raise HTTPException(500, detail={"message": "Metadata does not exist"})
    except ValidationError as error:
        logging.error("Get metadata raised ValidationError")
        log.event = "Get Metadata Request Failed"
        log.severity = 10
        log.log_id = "L0024"
        log.extension["message"] = "Request to get metadata failed"
        log.log()
        raise HTTPException(
            500, detail={"message": "Metadata was not file information"}
        )
    except Exception as error:
        logging.error(f"Unhandled error when getting metadata - error - {error}")
        log.event = "Get Metadata Request Failed"
        log.severity = 10
        log.log_id = "L0024"
        log.extension["message"] = "Request to get metadata failed"
        log.log()
        raise HTTPException(500, detail={"message": "Error when getting metadata"})

    logging.info("Get file metadata request was successful")
    log.event = "Get Metadata Request Successful"
    log.severity = 1
    log.log_id = "L0023"
    log.extension["message"] = "Get metadata was successful"
    log.log()

    response = Response(
        message="Got Metadata", metadata=metadata, connection_info=connection_info
    )

    return response


@router.delete("/deleteMetadata/{file_id}")
async def delete_file_metadata(
    request: Request,
    file_id: UUID,
    redis_connection: redis.Redis = Depends(dependency.get_redis),
):
    log: CommonEventFormat = CommonEventFormat(version="0.1.0")
    connection_info: ConnectionInformation = connection_service.connection_info(
        request=request
    )

    log.connection_id = connection_info.connection_id
    log.extension["src"] = connection_info.source_addr
    log.extension["host"] = connection_info.host_addr

    log.file_id = file_id

    try:
        metadata_deleted = await redis_service.delete_metadata(file_id=file_id, redis_connection=redis_connection)
    except (
        redis_exception.ConnectionError,
        redis_exception.TimeoutError,
        redis_exception.AuthenticationError,
        redis_exception.ResponseError,
        redis_exception.DataError,
        redis_exception.InvalidResponse,
    ) as error:
        logging.error(f"Connection Error to redis {error}")
        log.event = "Delete Metadata Storage Request Failed"
        log.severity = 10
        log.log_id = "L0026"
        log.extension["message"] = "Delete metadata storage request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Redis Error"})
    except asyncio.CancelledError as error:
        logging.error(f"Asyncio error {error}")
        log.event = "Delete Metadata Storage Request Failed"
        log.severity = 10
        log.log_id = "L0026"
        log.extension["message"] = "Delete metadata storage request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Asyncio Error"})
    except Exception as error:
        logging.error(f"Unhandled Error raised {error}")
        log.event = "Delete Metadata Storage Request Failed"
        log.severity = 10
        log.log_id = "L0026"
        log.extension["message"] = "Delete metadata storage request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Internal Error"})

    if not metadata_deleted:
        logging.info(f"Metadata NOT Deleted")
        log.event = "Delete Metadata Storage Request Failed"
        log.severity = 10
        log.log_id = "L0021"
        log.extension["message"] = "New metadata storage request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Metadata NOT Stored"})

    
    logging.info("Delete file metadata request was successful")
    log.event = "Delete Metadata Request Successful"
    log.severity = 1
    log.log_id = "L0025"
    log.extension["message"] = "Delete metadata was successful"
    log.log()

    return {
        "message": "Metadata Deleted"
        }
