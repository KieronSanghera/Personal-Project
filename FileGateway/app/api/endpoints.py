from fastapi import APIRouter, UploadFile, Request
from app.services import file_service, connection_service
from app.schemas.schemas import Response, FileInformation, ConnectionInformation
from uuid import uuid4

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Default"}

@router.post("/upload")
async def file_upload(file: UploadFile, request: Request):
    
    connection_info: ConnectionInformation = connection_service.connection_info(request=request)
    file_info: FileInformation = file_service.get_metadata(file=file)
    
    # with open(f"{uuid4()}", "wb") as f:
    #     contents = await file.read() 
    #     f.write(contents)
    
    response = Response(message="POST Upload", 
                        file_info=file_info, 
                        connection_info=connection_info)

    return response