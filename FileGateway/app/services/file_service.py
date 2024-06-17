from fastapi import UploadFile
from app.schemas.schemas import FileInformation

def get_metadata(file: UploadFile):
    metadata = FileInformation(
        filename=file.filename,
        filesize= file.size
    )
    return metadata
