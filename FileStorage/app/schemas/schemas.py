from pydantic import BaseModel, Field
from fastapi import Form
from uuid import UUID
from datetime import datetime
from dataclasses import dataclass

class FileInformation(BaseModel):
    """File Information Base Model"""
    file_id: UUID
    filename: str
    filesize: int = Field(ge=0)
    
    @classmethod
    def as_form(
        cls,
        file_id: UUID = Form(...),
        filename: str = Form(...),
        filesize: int= Form(...)
    ) -> "FileInformation": return cls(file_id=file_id, filename=filename, filesize=filesize)
    
