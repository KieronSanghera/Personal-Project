from fastapi import (
    APIRouter,
    UploadFile,
    Request,
    Depends,
    status,
    HTTPException,
)
from fastapi.responses import JSONResponse
from app.services import file_service, connection_service, metadata_service
from app.schemas.schemas import (
    FileInformation,
    ConnectionInformation,
    CommonEventFormat,
)
import logging
from pathlib import PosixPath
from app.config import configs

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Default"}


@router.post("/saveFile")
async def save_file(
    request: Request,
    file: UploadFile,
    file_data: FileInformation = Depends(FileInformation.as_form),
) -> JSONResponse:
    log: CommonEventFormat = CommonEventFormat(version="0.1.0")

    connection_info: ConnectionInformation = connection_service.connection_info(
        request=request
    )

    log.connection_id = connection_info.connection_id
    log.extension["src"] = connection_info.source_addr
    log.extension["host"] = connection_info.host_addr

    log.file_id = file_data.file_id
    file_data.location = PosixPath(f"{configs.store_dir}/{file_data.file_id}").resolve()

    
    metadata_stored = metadata_service.new_metadata_request(file_data=file_data)

    if not metadata_stored:
        logging.error(f"Metadata could NOT be stored")
        log.event = "File Storage Failed"
        log.severity = 10
        log.log_id = "L0011"
        log.extension["message"] = "Error Occurred when storing due to Metadata Storage request"
        log.log()
        raise HTTPException(500, detail={"message": "Error making request to Metadata Storage"})

    try:
        file_service.store_file(file=file, file_info=file_data)
        response_content = {"message": "File successfully store"}
    except OSError as error:
        logging.error(f"Storage OSError - error - {error}")
        log.event = "File Storage Failed"
        log.severity = 10
        log.log_id = "L0011"
        log.extension["message"] = "Error Occurred when storing due to OSError"
        log.log()
        file_service.failed_file(file_data.location)
        raise HTTPException(500, detail={"message": "Error when storing file"})
    except TypeError as error:
        logging.error(f"Storage TypeError - error - {error}")
        log.event = "File Storage Failed"
        log.severity = 10
        log.log_id = "L0011"
        log.extension["message"] = "Error Occurred when storing due to TypeError"
        log.log()
        file_service.failed_file(file_data.location)
        raise HTTPException(500, detail={"message": "Error when storing file"})
    except MemoryError as error:
        logging.error(f"Storage Memory - error - {error}")
        log.event = "File Storage Failed"
        log.severity = 10
        log.log_id = "L0011"
        log.extension["message"] = "Error Occurred when storing due to Memory"
        log.log()
        file_service.failed_file(file_data.location)
        raise HTTPException(500, detail={"message": "Error when storing file"})
    except Exception as error:
        logging.error(f"Storage Unhandled Error - error - {error}")
        log.event = "File Storage Failed"
        log.severity = 10
        log.log_id = "L0011"
        log.extension["message"] = (
            "Error Occurred when storing due to an Unhandled Error"
        )
        log.log()
        file_service.failed_file(file_data.location)
        raise HTTPException(500, detail={"message": "Error when storing file"})    

    logging.debug("Store File was successful")
    log.event = "File Storage Success"
    log.severity = 5
    log.log_id = "L0010"
    log.extension["message"] = "File was successfully stored"
    log.log()

    response = JSONResponse(
        status_code=status.HTTP_201_CREATED, content=response_content
    )

    return response
