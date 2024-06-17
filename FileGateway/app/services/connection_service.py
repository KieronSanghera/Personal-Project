from fastapi import Request
from uuid import uuid4
from app.schemas.schemas import ConnectionInformation

def connection_info(request: Request):
    info = ConnectionInformation(
        connection_id=uuid4(),
        source_addr=request.client.host)
    return info
