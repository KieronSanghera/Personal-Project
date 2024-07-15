from fastapi import UploadFile
from app.schemas.schemas import FileInformation
from uuid import uuid4
import logging

def get_filedata(file: UploadFile):
    filedata = FileInformation(filename=file.filename,
                               filesize= file.size,
                               file_id=uuid4())
    return filedata
