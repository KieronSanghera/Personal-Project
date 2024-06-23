from fastapi import UploadFile
import shutil
import logging
from app.schemas.schemas import FileInformation
from pathlib import Path


def store_file(file: UploadFile, file_info: FileInformation) -> bool:
    file_info.location = Path(f"./{file_info.file_id}")
    with open(file_info.location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    logging.info("File successfully stored")
