from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.responses import FileResponse
from uuid import UUID
import os 
from app.services import file_service, connection_service
from app.schemas.schemas import FileInformation, CommonEventFormat, ConnectionInformation
import requests
import json
import logging

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Download File Request Failed"}


@router.get("/download/{file_id}")
async def download_file(request: Request, file_id: UUID):
    log: CommonEventFormat = CommonEventFormat(version="0.1.0")
    connection_info: ConnectionInformation = connection_service.connection_info(
        request=request
        
    )
    
    log.connection_id = connection_info.connection_id
    log.extension["src"] = connection_info.source_addr
    log.extension["host"] = connection_info.host_addr
    
    log.file_id = file_id
    
    try:
        file_info: FileInformation = file_service.get_file_info(file_id=file_id)
    except requests.exceptions.ConnectionError as error :
        logging.error(f"Connection Error to Metadata Storage {error}")
        log.event = "Download File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata connection failed"
        log.log()
        raise HTTPException(500, detail={"message": "Download File Request Failed"})
    except requests.exceptions.Timeout as error:
        logging.error(f"Connection Timeout to Metadata Storage {error}")
        log.event = "Download File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata connection timeout"
        log.log()
        raise HTTPException(500, detail={"message": "Download File Request Failed"})
    except requests.exceptions.HTTPError as error:
        logging.error(f"HTTP Error for Metadata Storage {error}")
        log.event = "Download File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata connection failed"
        log.log()
        raise HTTPException(500, detail={"message": "Download File Request Failed"})
    except requests.exceptions.RequestException as error:
        logging.error(f"Request Error for Metadata Storage {error}")
        log.event = "Download File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Download File Request Failed"})
    except json.JSONDecodeError as error:
        logging.error(f"JSON Decode Error for Metadata {error}")
        log.event = "Download File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Download File Request Failed"})
    except UnicodeDecodeError as error:
        logging.error(f"Unicode Decode Error for Metadata {error}")
        log.event = "Download File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Download File Request Failed"})
    except Exception as error:
        logging.error(f"Unhandled Exception for get metadata {error}")
        log.event = "Download File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Download File Request Failed"})
    
    logging.debug("Download File request was successful")
    log.event = "Download File Request Successful"
    log.severity = 5
    log.log_id = "L0030"
    log.extension["message"] = "File was downloaded successfully"
    log.log()

    
    name = file_info.filename
    return FileResponse(path=file_info.location,
                        filename=str(name),
                        media_type="application/octet-stream",
                        )
    
@router.delete("/delete/{file_id}")
def delete(request: Request, file_id: UUID):
    log: CommonEventFormat = CommonEventFormat(version="0.1.0")
    connection_info: ConnectionInformation = connection_service.connection_info(
        request=request
        
    )
    
    log.connection_id = connection_info.connection_id
    log.extension["src"] = connection_info.source_addr
    log.extension["host"] = connection_info.host_addr
    
    log.file_id = file_id
    
    try:
        file_info: FileInformation = file_service.get_file_info(file_id=file_id)
        deleted = file_service.delete_file(file_info=file_info)
    except requests.exceptions.ConnectionError as error :
        logging.error(f"Connection Error to Metadata Storage {error}")
        log.event = "Delete File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata connection failed"
        log.log()
        raise HTTPException(500, detail={"message": "Delete File Request Failed"})
    except requests.exceptions.Timeout as error:
        logging.error(f"Connection Timeout to Metadata Storage {error}")
        log.event = "Delete File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata connection timeout"
        log.log()
        raise HTTPException(500, detail={"message": "Delete File Request Failed"})
    except requests.exceptions.HTTPError as error:
        logging.error(f"HTTP Error for Metadata Storage {error}")
        log.event = "Delete File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata connection failed"
        log.log()
        raise HTTPException(500, detail={"message": "Delete File Request Failed"})
    except requests.exceptions.RequestException as error:
        logging.error(f"Request Error for Metadata Storage {error}")
        log.event = "Delete File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Delete File Request Failed"})
    except json.JSONDecodeError as error:
        logging.error(f"JSON Decode Error for Metadata {error}")
        log.event = "Delete File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Delete File Request Failed"})
    except UnicodeDecodeError as error:
        logging.error(f"Unicode Decode Error for Metadata {error}")
        log.event = "Delete File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Delete File Request Failed"})
    except Exception as error:
        logging.error(f"Unhandled Exception for get metadata {error}")
        log.event = "Delete File Request Failed"
        log.severity = 10
        log.log_id = "L0031"
        log.extension["message"] = "Get metadata request failed"
        log.log()
        raise HTTPException(500, detail={"message": "Delete File Request Failed"})
    
    if deleted is False:
        logging.debug("Delete File request failed")
        log.event = "Delete File Request Failed"
        log.severity = 5
        log.log_id = "L0033"
        log.extension["message"] = "File was NOT deleted"
        log.log()
        raise HTTPException(500, detail={"message": "Delete File Request Failed"})

        
    logging.debug("Delete File request was successful")
    log.event = "Delete File Request Successful"
    log.severity = 5
    log.log_id = "L0032"
    log.extension["message"] = "File was deleted successfully"
    log.log()
    return Response(status_code=200, content="File Successfully Deleted")