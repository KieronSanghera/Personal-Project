from app.main import app
from app.schemas.schemas import FileInformation
from fastapi.testclient import TestClient
from fastapi import UploadFile
from pytest import fixture
from httpx import Response
from uuid import uuid4
from unittest.mock import patch, MagicMock
from file_factory import UploadFileFactory
import requests
import json


class MockedResponse:
    def __init__(self, status_code):
        self.status_code = status_code

@fixture(autouse=True)
def setup_test_client():
    """Setup class fixture"""
    client: TestClient = TestClient(app)
    yield client


class TestUploadSuccess:
    
    def test_successful_upload(self, setup_test_client):
        test_client: TestClient = setup_test_client
        mock_response: requests.Response = MockedResponse(status_code=201)
        mock_file: UploadFile = UploadFileFactory.create()
        
        with patch("app.services.file_storage_service.store_file", MagicMock(return_value=mock_response)):
            response: Response = test_client.post(
                url="/upload",
                files={"file": mock_file.file}
            )
            print(response)
    
    
class TestUploadFailure:
    
    def test_failure_upload_file_storage_response_not_201(self, setup_test_client):
        test_client: TestClient = setup_test_client
        mock_response: requests.Response = MockedResponse(status_code=500)
        mock_file: UploadFile = UploadFileFactory.create()
        
        with patch("app.services.file_storage_service.store_file", MagicMock(return_value=mock_response)):
            response: Response = test_client.post(
                url="/upload",
                files={"file": mock_file.file}
            )
            print(response)
        
    def test_upload_store_CONNECTIONERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client
        mock_file: UploadFile = UploadFileFactory.create()
        
        with patch("app.services.file_storage_service.store_file", MagicMock(side_effect=requests.exceptions.ConnectionError())):
            response: Response = test_client.post(
                url="/upload",
                files={"file": mock_file.file}
            )
            
        contents = json.loads(response.content.decode())
        
        assert response.status_code == 500
        assert contents["detail"] == {"message": "No connection to File Storage"}
            
        
        