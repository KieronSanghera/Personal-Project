from app.services import file_service
from file_factory import UploadFileFactory
from app.schemas.schemas import FileInformation
from fastapi import UploadFile

class TestGetFileDataSuccess:
    
    def test_successful_get_filedata(self):
        file: UploadFile = UploadFileFactory.create()
        filedata: FileInformation = file_service.get_filedata(file=file)
        
        assert filedata.filename == file.filename
        assert filedata.filesize == file.size