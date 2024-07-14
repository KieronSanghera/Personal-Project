from app.main import app
from app.dependencies import dependency
from app.schemas.schemas import FileInformation
from app.exceptions.redis_exceptions import RedisException
from fastapi.testclient import TestClient
from pytest import fixture
from httpx import Response
from uuid import uuid4
from unittest.mock import patch, AsyncMock
from file_factory import FileInformationFactory
import json
from pydantic_core import ValidationError


@fixture(autouse=True)
def setup_test_client():
    """Setup class fixture"""
    app.dependency_overrides[dependency.get_redis] = lambda: ""
    client: TestClient = TestClient(app)
    yield client


class TestGetMetadataSuccess:

    def test_successful_get_metadata(self, setup_test_client):
        test_client: TestClient = setup_test_client

        redis_metadata: FileInformation = FileInformationFactory.create()

        with patch(
            "app.services.redis_service.get_metadata",
            AsyncMock(return_value=redis_metadata),
        ):
            response: Response = test_client.get(url=f"/getMetadata/{uuid4()}")

        contents = json.loads(response.content.decode())
        metadata = contents["metadata"]

        assert response.status_code == 200
        assert contents["message"] == "Get Metadata"
        assert metadata == redis_metadata.model_dump_database()


class TestGetMetadataFailure:

    def test_failed_get_metadata_UNICODEDECODEERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client

        with patch(
            "app.services.redis_service.get_metadata",
            AsyncMock(side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "pytest")),
        ):
            response: Response = test_client.get(url=f"/getMetadata/{uuid4()}")

        contents = json.loads(response.content.decode())
        assert response.status_code == 500
        assert contents["detail"] == {"message": "Redis Decode Error"}

    def test_failed_get_metadata_JSONDECODEERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client

        with patch(
            "app.services.redis_service.get_metadata",
            AsyncMock(side_effect=json.JSONDecodeError("", "", 0)),
        ):
            response: Response = test_client.get(url=f"/getMetadata/{uuid4()}")

        contents = json.loads(response.content.decode())
        assert response.status_code == 500
        assert contents["detail"] == {"message": "Redis/Metadata Error"}

    def test_failed_get_metadata_REDISEXCEPTION(self, setup_test_client):
        test_client: TestClient = setup_test_client

        with patch(
            "app.services.redis_service.get_metadata",
            AsyncMock(side_effect=RedisException("")),
        ):
            response: Response = test_client.get(url=f"/getMetadata/{uuid4()}")

        contents = json.loads(response.content.decode())
        assert response.status_code == 500
        assert contents["detail"] == {"message": "Metadata does not exist"}

    def test_failed_get_metadata_VALIDATIONERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client

        with patch(
            "app.services.redis_service.get_metadata",
            AsyncMock(side_effect=ValidationError.from_exception_data("", [])),
        ):
            response: Response = test_client.get(url=f"/getMetadata/{uuid4()}")

        contents = json.loads(response.content.decode())
        assert response.status_code == 500
        assert contents["detail"] == {"message": "Metadata was not file information"}

    def test_failed_get_metadata_EXCEPTION(self, setup_test_client):
        test_client: TestClient = setup_test_client

        with patch(
            "app.services.redis_service.get_metadata",
            AsyncMock(side_effect=Exception()),
        ):
            response: Response = test_client.get(url=f"/getMetadata/{uuid4()}")

        contents = json.loads(response.content.decode())
        assert response.status_code == 500
        assert contents["detail"] == {"message": "Error when getting metadata"}
