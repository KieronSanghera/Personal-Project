from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
        
class ConnectionInformation(BaseModel):
    """Connection Information Base Model"""
    connection_id: UUID 
    source_addr: str = "Unknown"
    request_time: datetime = datetime.now()
    
class FileInformation(BaseModel):
    """File Information Base Model"""
    file_id: UUID
    filename: str
    filesize: int = Field(ge=0)

class Response(BaseModel):
    """Response Base Model"""
    
    message: str
    file_info: FileInformation
    connection_info: ConnectionInformation
    