from fastapi import APIRouter, UploadFile, Request
from app.services import file_service, connection_service
from uuid import uuid4

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Default"}

@router.post("/upload")
async def file_upload(file: UploadFile, request: Request):
    
    connection_info = connection_service.connection_info(request=request)
    
    with open(f"{uuid4()}", "wb") as f:
        contents = await file.read() 
        f.write(contents)
    
    return {"message": "POST Upload",
            "filename": file.filename,
            "filesize": file.size,
            "connection_info": connection_info}