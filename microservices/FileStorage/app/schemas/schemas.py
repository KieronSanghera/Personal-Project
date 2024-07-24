from pydantic import BaseModel, Field, model_validator
from pydantic.networks import IPvAnyAddress
from fastapi import Form
from uuid import UUID
from datetime import datetime
from dataclasses import dataclass
from typing import Union, Optional
import logging
from pathlib import PosixPath
from config import configs

class ConnectionInformation(BaseModel):
    """Connection Information Base Model"""

    connection_id: UUID
    source_addr: Union[IPvAnyAddress, str] = "Unknown"
    request_time: datetime = datetime.now()
    host_addr: IPvAnyAddress = "127.0.0.1"


class FileInformation(BaseModel):
    """File Information Base Model"""

    file_id: UUID
    filename: str
    filesize: int = Field(ge=0)
    location: Optional[PosixPath] = None
    
    @model_validator(mode="after")
    def set_location(self):
        self.location = PosixPath(f"{configs.store_dir}/{self.file_id}").resolve()
        return self
    
    @classmethod
    def as_form(
        cls,
        file_id: UUID = Form(...),
        filename: str = Form(...),
        filesize: int = Form(...),
    ) -> "FileInformation":
        return cls(file_id=file_id, filename=filename, filesize=filesize)


class CommonEventFormat(BaseModel):
    """CEF Base Model"""

    vendor: str = "Project"
    service: str = "FileStorage"
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    log_id: str = Field(pattern=r"^L\d+$", default="L0")
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