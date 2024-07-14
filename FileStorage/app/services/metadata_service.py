from requests import Response
import requests
from app.schemas.schemas import FileInformation
import logging
import json

def new_metadata_request(file_data: FileInformation) -> bool:
    metadata_response: Response = requests.post(
        url="http://localhost:8002/newMetadata",
        data=file_data.model_dump()
    )
    
    if metadata_response.status_code == 201:
        logging.debug("Metadata Stored")
        return True
    
    contents = json.loads(metadata_response.content.decode())
    logging.debug(f"Metadata NOT Stored - message - {contents['detail']}")
    return False
    