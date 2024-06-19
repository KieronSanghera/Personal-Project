from fastapi import APIRouter, UploadFile, Request, HTTPException
from app.services import file_service, connection_service
from app.schemas.schemas import Response, FileInformation, ConnectionInformation
import requests

router = APIRouter()

@router.get("/")
async def root():

    return {"message": "Default"}

@router.post("/upload")
async def file_upload(request: Request, file: UploadFile) -> Response:
    connection_info: ConnectionInformation = connection_service.connection_info(request=request)
    file_info: FileInformation = file_service.get_metadata(file=file)
    
    requests.post(url="http://localhost:8000/saveFile",
                  data={"file_id": file_info.file_id, "filename": file_info.filename, "filesize": file_info.filesize},
                  files={"file": file.file})
        
    response = Response(message="POST Upload", 
                        file_info=file_info, 
                        connection_info=connection_info)

    return response