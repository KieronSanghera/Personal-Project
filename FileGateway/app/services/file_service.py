from fastapi import UploadFile
from app.schemas.schemas import FileInformation
from uuid import uuid4

def get_metadata(file: UploadFile):
    metadata = FileInformation(filename=file.filename,
                               filesize= file.size,
                               file_id=uuid4())
    return metadata
