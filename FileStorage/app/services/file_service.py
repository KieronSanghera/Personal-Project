from fastapi import UploadFile
import shutil
import logging
from app.schemas.schemas import FileInformation
from pathlib import Path

def get_metadata(file: UploadFile):
    metadata = {
        "filename": file.filename,
        "filesize": file.size
    }
    return metadata


def store_file(file: UploadFile, file_info: FileInformation) -> bool:
    file_location: Path = f"./{file_info.file_id}"
    logging.info(f"{file_location=}")
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logging.info("File successfully stored")
        return True
    except Exception as error:
        logging.error(f"Error has occurred information: {error}")
        return False