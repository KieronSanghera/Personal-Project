from fastapi import APIRouter, UploadFile, Request, HTTPException, Response
from app.services import file_service, connection_service
from app.schemas.schemas import (
    Response,
    FileInformation,
    ConnectionInformation,
    CommonEventFormat,
)
import requests
from requests import Response as APIResponse
import logging
from uuid import uuid4


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Default"}


@router.post("/upload")
async def file_upload(request: Request, file: UploadFile) -> Response:
    log: CommonEventFormat = CommonEventFormat(version="0.1.0")
    log_info = {}
    connection_info: ConnectionInformation = connection_service.connection_info(
        request=request
    )
    file_info: FileInformation = file_service.get_metadata(file=file)
    
    log_info["src"] = connection_info.source_addr

    store_file: APIResponse = requests.post(
        url="http://localhost:8000/saveFile",
        data={
            "file_id": file_info.file_id,
            "filename": file_info.filename,
            "filesize": file_info.filesize,
        },
        files={"file": (file.filename, file.file, file.content_type)},
    )

    if store_file.status_code == 201:
        logging.debug("File store request was successful")
        log.event = "File store request successful"
        log.severity = 1
        log.log_id = "L0001"
        log.log()

    response = Response(
        message="POST Upload", file_info=file_info, connection_info=connection_info
    )

    return response
