from pydantic import BaseModel, Field
from fastapi import Form
from typing import Union, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
import logging
from pathlib import PosixPath


class FileInformation(BaseModel):
    """File Information Base Model"""

    file_id: UUID
    filename: str
    filesize: int = Field(ge=0)
    location: PosixPath

    @classmethod
    def as_form(
        cls,
        file_id: UUID = Form(...),
        filename: str = Form(...),
        filesize: int = Form(...),
        location: PosixPath = Form(...),
    ) -> "FileInformation":
        return cls(file_id=file_id, filename=filename, filesize=filesize, location=location)

    def model_dump_database(self) -> Dict[str, Any]:
        primitive_dict = {}
        for field_name in self.model_fields:
            field_value = getattr(self, field_name)
            primitive_value = self._to_primitive(field_value)
            primitive_dict[field_name] = primitive_value
        return primitive_dict

    @staticmethod
    def _to_primitive(value: Any) -> Any:
        if isinstance(value, (int, float, str, bool)):
            return value
        elif isinstance(value, dict):
            return {k: FileInformation._to_primitive(v) for k, v in value.items()}
        elif isinstance(value, (list, set, tuple)):
            return [FileInformation._to_primitive(item) for item in value]
        elif hasattr(value, "model_dump"):
            return value.model_dump()
        else:
            return str(value)

class CommonEventFormat(BaseModel):
    """CEF Base Model"""

    vendor: str = "Project"
    service: str = "FileGateway"
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
