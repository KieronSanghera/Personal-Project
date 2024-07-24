from fastapi import UploadFile
import shutil
import logging
from app.schemas.schemas import FileInformation
from pathlib import PosixPath


def store_file(file: UploadFile, file_info: FileInformation) -> bool:
    with open(file_info.location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    logging.info("File successfully stored")


def failed_file(file_path: PosixPath):
    try:
        if file_path.is_file():
            file_path.unlink(missing_ok=True)
    except PermissionError as error:
        logging.error(f"Permission Error when removing file - error - {error}")
        return False
    except Exception as error:
        logging.error(f"Error: {error}")
        return False
