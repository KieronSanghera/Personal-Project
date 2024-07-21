from fastapi import Request
from uuid import uuid4
from app.schemas.schemas import ConnectionInformation
import socket
import logging


def connection_info(request: Request):
    info = ConnectionInformation(connection_id=uuid4(), source_addr=request.client.host, host_addr=get_host_ip())
    return info


def get_host_ip():
    try:
        # Connect to an external server to get the current IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        ip = "Unable to get IP address"
        print(f"Error: {e}")
    return ip
