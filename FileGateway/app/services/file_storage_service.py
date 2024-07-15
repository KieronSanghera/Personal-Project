from requests import Response
import requests
from app.config import configs
import logging


def store_file(data: dict, files: dict):
    store_file: Response = requests.post(
        url=f"http://{configs.file_storage_addr}:{configs.file_storage_port}/saveFile",
        data=data,
        files=files,
    )
    logging.info(store_file.content)

    return store_file
