from uuid import UUID
import requests
from app.config import configs
import json
from app.schemas.schemas import FileInformation
import logging

def delete_file(file_info: FileInformation):
    file_path = file_info.location
    try:
        if file_path.is_file():
            file_path.unlink(missing_ok=True)
    except PermissionError as error:
        logging.error(f"Permission Error when removing file - error - {error}")
        return False
    except Exception as error:
        logging.error(f"Error: {error}")
        return False