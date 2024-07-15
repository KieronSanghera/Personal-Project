from requests import Response
import requests
import logging


def store_file(data: dict, files: dict):
    store_file: Response = requests.post(
        url="http://localhost:8080/saveFile",
        data=data,
        files=files,
    )
    logging.info(store_file.content)

    return store_file
