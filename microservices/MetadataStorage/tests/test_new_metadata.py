import redis.exceptions
from app.main import app
from app.dependencies import dependency
from app.schemas.schemas import FileInformation
from fastapi.testclient import TestClient
from pytest import fixture
from unittest.mock import patch, AsyncMock
from file_factory import FileInformationFactory
import json
import redis
import asyncio

@fixture(autouse=True)
def setup_test_client():
    """Setup class fixture"""
    app.dependency_overrides[dependency.get_redis] = lambda: ""
    client: TestClient = TestClient(app)
    yield client


class TestNewMetadataSuccess:

    def test_successful_new_metadata(self, setup_test_client):
        test_client: TestClient = setup_test_client
        form_data: FileInformation = FileInformationFactory.create_dict()

        with patch(
            "app.services.redis_service.new_metadata",
            AsyncMock(return_value=True),
        ):
            response = test_client.post(url="/newMetadata", data=form_data)
            
        content = json.loads(response.content.decode())
            
        assert response.status_code == 201
        assert content["message"] == "Metadata Stored"
        
class TestNewMetadataFailure:
    
    def test_failed_new_metadata_not_stored(self, setup_test_client):
        test_client: TestClient = setup_test_client
        form_data: FileInformation = FileInformationFactory.create_dict()

        with patch(
            "app.services.redis_service.new_metadata",
            AsyncMock(return_value=False),
        ):
            response = test_client.post(url="/newMetadata", data=form_data)
            
        content = json.loads(response.content.decode())
            
        assert response.status_code == 500
        assert content["detail"] == {"message": "Metadata NOT Stored"}
        
    def test_failed_new_metadata_REDISERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client
        form_data: FileInformation = FileInformationFactory.create_dict()

        
        with patch("app.services.redis_service.new_metadata", AsyncMock(side_effect=redis.exceptions.ConnectionError())):
            response = test_client.post(url="/newMetadata", data=form_data)
        
        content = json.loads(response.content.decode())

        assert response.status_code == 500
        assert content["detail"] == {"message": "Redis Error"}
        
    def test_failed_new_metadata_ASYNCCANCELLEDERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client
        form_data: FileInformation = FileInformationFactory.create_dict()

        
        with patch("app.services.redis_service.new_metadata", AsyncMock(side_effect=asyncio.CancelledError())):
            response = test_client.post(url="/newMetadata", data=form_data)
        
        content = json.loads(response.content.decode())

        assert response.status_code == 500
        assert content["detail"] == {"message": "Asyncio Error"}
        
    def test_failed_new_metadata_EXCEPTION(self, setup_test_client):
        test_client: TestClient = setup_test_client
        form_data: FileInformation = FileInformationFactory.create_dict()

        
        with patch("app.services.redis_service.new_metadata", AsyncMock(side_effect=Exception())):
            response = test_client.post(url="/newMetadata", data=form_data)
        
        content = json.loads(response.content.decode())

        assert response.status_code == 500
        assert content["detail"] == {"message": "Internal Error"}