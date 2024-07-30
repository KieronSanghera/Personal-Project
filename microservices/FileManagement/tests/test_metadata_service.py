from .file_factory import FileInformationFactory, UploadFileFactory
from unittest.mock import patch, MagicMock
from app.services import metadata_service
from app.schemas.schemas import FileInformation
import os
from pathlib import PosixPath
import pytest
from pytest import fixture
import responses
import json

class TestMetadataServiceSuccess:
    
    @responses.activate
    def test_get_file_info_success(self):
        file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        response_metadata = '{"metadata": {  "file_id": "1564fd75-fb2a-48ad-ace3-7254ae16b4b1", "filename": "surface.txt",  "filesize": "21",  "location": "/tmp" }}'
        response_dict = json.loads(response_metadata)
        response_file_info = FileInformation(**response_dict["metadata"])
        responses.add(
            method=responses.GET,
            url = f"http://localhost:80/getMetadata/{file_id}",
            status = 200,
            body = response_metadata,
        )
        data = metadata_service.get_file_info(file_id=file_id)
        assert response_file_info == data

    @responses.activate
    def test_delete_metadata_success(self):
        file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        responses.add(
            method=responses.DELETE,
            url = f"http://localhost:80/deleteMetadata/{file_id}",
            status = 200,
        )
        response = metadata_service.delete_metadata(file_id=file_id)
        assert response is True
        
class TestMetadataServiceFailure:

    @responses.activate
    def test_get_file_info_failed(self):
        file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        response_metadata = '{"metadata": {  "file_id": "1564fd75-fb2a-48ad-ace3-7254ae16b4b1", "filename": "surface.txt",  "filesize": "21",  "location": "/tmp" }}'
        responses.add(
            method=responses.GET,
            url = f"http://localhost:80/getMetadata/{file_id}",
            status = 500,
            body = response_metadata,
        )
        with pytest.raises(Exception):
            metadata_service.get_file_info(file_id=file_id)
            
    @responses.activate
    def test_delete_metadata_success(self):
        file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        responses.add(
            method=responses.DELETE,
            url = f"http://localhost:80/deleteMetadata/{file_id}",
            status = 500,
        )
        with pytest.raises(Exception):
            metadata_service.delete_metadata(file_id=file_id)
        
