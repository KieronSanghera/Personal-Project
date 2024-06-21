from fastapi import APIRouter, UploadFile, Request, Depends, Response, status
from fastapi.responses import JSONResponse
from app.services import file_service, connection_service
from app.schemas.schemas import FileInformation
from pathlib import Path
from uuid import uuid4
import requests
from typing import Annotated
import logging
import shutil


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Default"}

@router.post("/saveFile")
async def save_file(request: Request, file: UploadFile, form_data: FileInformation = Depends(FileInformation.as_form)):
    
    if file_service.store_file(file=file, file_info=form_data):
        response_content = {"message": "File successfully store"}
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_content)
    
    
    
    
    