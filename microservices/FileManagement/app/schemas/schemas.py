from pydantic import BaseModel, Field
from typing import Union
from uuid import UUID
from datetime import datetime
import logging
from pathlib import PosixPath
from pydantic import IPvAnyAddress


class ConnectionInformation(BaseModel):
    """Connection Information Base Model"""

    connection_id: UUID
    source_addr: str = "Unknown"
    request_time: datetime = datetime.now()
    host_addr: IPvAnyAddress = "127.0.0.1"


class FileInformation(BaseModel):
    """File Information Base Model"""

    file_id: UUID
    filename: str
    filesize: int = Field(ge=0)
    location: PosixPath


class CommonEventFormat(BaseModel):
    """CEF Base Model"""

    vendor: str = "Project"
    service: str = "FileRelease"
    version: str = Field(pattern="^\d+\.\d+\.\d+$")
    log_id: str = Field(pattern="^L\d+$", default="L0")
    event: str = "No Event"
    severity: int = Field(ge=0, le=10, default=0)
    timestamp: datetime = datetime.now()
    connection_id: Union[UUID, str] = "Not set"
    file_id: Union[UUID, str] = "Not set"
    extension: dict = {}

    def log(self) -> str:
        base: str = (
            f"CEF:1|{self.vendor}|{self.service}|{self.version}|{self.log_id}|{self.event}|{self.severity}|{self.timestamp}|conn_id={self.connection_id}|file_id={self.file_id}|"
        )
        extensions_list = []
        for key, value in self.extension.items():
            extensions_list.append(f"{key}={value} ")
        extensions_str = "".join(extensions_list)
        logging.info("".join([base, extensions_str]))
