from fastapi import APIRouter, UploadFile, Request, HTTPException
from app.services import file_service, connection_service, file_storage_service
from app.schemas.schemas import (
    Response,
    FileInformation,
    ConnectionInformation,
    CommonEventFormat,
)
import requests
from requests import Response as APIResponse
import logging

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Default"}


@router.post("/upload")
async def file_upload(request: Request, file: UploadFile) -> Response:
    log: CommonEventFormat = CommonEventFormat(version="0.1.0")
    connection_info: ConnectionInformation = connection_service.connection_info(
        request=request
    )
    file_info: FileInformation = file_service.get_filedata(file=file)

    log.connection_id = connection_info.connection_id
    log.extension["src"] = connection_info.source_addr
    log.extension["host"] = connection_info.host_addr

    log.file_id = file_info.file_id

    try:
        store_file = file_storage_service.store_file(
            data={
                "file_id": file_info.file_id,
                "filename": file_info.filename,
                "filesize": file_info.filesize,
            },
            files={"file": (file.filename, file.file, file.content_type)},
        )
    except requests.exceptions.ConnectionError as error:
        logging.error(f"Connection to File Storage failed - error - {error}")
        log.event = "File Upload Failed"
        log.severity = 10
        log.log_id = "L0001"
        log.extension["message"] = "Connection to File Storage failed"
        log.log()
        raise HTTPException(500, detail={"message": "No connection to File Storage"})

    if store_file.status_code != 201:
        logging.debug(f"File Storage response was NOT 201")
        log.event = "File Upload Failed"
        log.severity = 5
        log.log_id = "L0001"
        log.extension["message"] = "File Storage response was NOT 201"
        log.log()
        raise HTTPException(500, detail={"message": "File could NOT be stored"})

    logging.info("File Storage request was successful")
    log.event = "File Upload Successful"
    log.severity = 1
    log.log_id = "L0000"
    log.extension["message"] = "Connection to File Storage successful"
    log.log()

    response = Response(
        message="POST Upload", file_info=file_info, connection_info=connection_info
    )

    return response
