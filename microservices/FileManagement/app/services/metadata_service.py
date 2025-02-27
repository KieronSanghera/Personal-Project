from uuid import UUID
import requests
from app.config import configs
import json
from app.schemas.schemas import FileInformation
import logging

def get_file_info(file_id: UUID):
    response = requests.get(
        f"http://{configs.metadata_storage_addr}:{configs.metadata_storage_port}/getMetadata/{file_id}"
    )
    if response.status_code != 200:
        raise Exception
    
    data = json.loads(response.content.decode("utf-8"))
    metadata = FileInformation(**data["metadata"])
    return metadata

def delete_metadata(file_id: UUID):
    response = requests.delete(
        f"http://{configs.metadata_storage_addr}:{configs.metadata_storage_port}/deleteMetadata/{file_id}"
    )
    if response.status_code != 200:
        raise Exception
    return True
    