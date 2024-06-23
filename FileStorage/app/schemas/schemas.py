from pydantic import BaseModel, Field
from fastapi import Form
from uuid import UUID
from datetime import datetime
from dataclasses import dataclass
from typing import Union, Optional
import logging
from pathlib import Path


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
    location: Optional[Path] = None

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
