from fastapi import Request

def connection_info(request: Request):
    info = {
        "source_addr": request.client.host
    }
    return info
