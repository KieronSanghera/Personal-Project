from fastapi.testclient import TestClient
from pytest import fixture
from app.main import app
from uuid import uuid4
from file_factory import FileInformationFactory
from unittest.mock import patch, MagicMock
import requests
import json
from pathlib import PosixPath


@fixture(autouse=True)
def setup_test_client(tmp_path):
    """Setup class fixture"""
    client: TestClient = TestClient(app)
    path: PosixPath = tmp_path / "test_file"
    path.mkdir()
    file = path / f"{uuid4()}"
    file.write_text("Test file with some fake content")
    yield client, file


class TestDeleteSuccess:

    def test_download_success(self, setup_test_client):
        test_client: TestClient
        file: PosixPath
        test_client, file = setup_test_client
        file_id = file.name
        fake_file_info = FileInformationFactory.create(file_id=file_id, location=file)

        with patch(
            "app.services.file_service.get_file_info",
            MagicMock(return_value=fake_file_info),
        ):
            response = test_client.get(url=f"/download/{file_id}")

        assert response.status_code == 200
        assert response.content.decode("utf-8") == "Test file with some fake content"


class TestDownloadFailure:

    def test_delete_failure_CONNECTIONERROR(self, setup_test_client):
        test_client: TestClient
        file: PosixPath
        test_client, file = setup_test_client
        file_id = file.name
        fake_file_info = FileInformationFactory.create(file_id=file_id, location=file)

        with patch(
            "app.services.file_service.get_file_info",
            MagicMock(side_effect=requests.exceptions.ConnectionError),
        ):
            response = test_client.get(url=f"/download/{file_id}")

        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail": {"message": "Download File Request Failed"}}

    def test_delete_failure_TIMEOUT(self, setup_test_client):
        test_client: TestClient
        file: PosixPath
        test_client, file = setup_test_client
        file_id = file.name
        fake_file_info = FileInformationFactory.create(file_id=file_id, location=file)

        with patch(
            "app.services.file_service.get_file_info",
            MagicMock(side_effect=requests.exceptions.Timeout),
        ):
            response = test_client.get(url=f"/download/{file_id}")

        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail": {"message": "Download File Request Failed"}}

    def test_delete_failure_HTTPERROR(self, setup_test_client):
        test_client: TestClient
        file: PosixPath
        test_client, file = setup_test_client
        file_id = file.name
        fake_file_info = FileInformationFactory.create(file_id=file_id, location=file)

        with patch(
            "app.services.file_service.get_file_info",
            MagicMock(side_effect=requests.exceptions.HTTPError),
        ):
            response = test_client.get(url=f"/download/{file_id}")
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail": {"message": "Download File Request Failed"}}

    def test_delete_failure_REQUESTEXCEPTION(self, setup_test_client):
        test_client: TestClient
        file: PosixPath
        test_client, file = setup_test_client
        file_id = file.name
        fake_file_info = FileInformationFactory.create(file_id=file_id, location=file)

        with patch(
            "app.services.file_service.get_file_info",
            MagicMock(side_effect=requests.exceptions.RequestException),
        ):
            response = test_client.get(url=f"/download/{file_id}")
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail": {"message": "Download File Request Failed"}}

    def test_delete_failure_JSONDECODEERROR(self, setup_test_client):
        test_client: TestClient
        file: PosixPath
        test_client, file = setup_test_client
        file_id = file.name
        fake_file_info = FileInformationFactory.create(file_id=file_id, location=file)

        with patch(
            "app.services.file_service.get_file_info",
            MagicMock(side_effect=json.JSONDecodeError("", "", 0)),
        ):
            response = test_client.get(url=f"/download/{file_id}")
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail": {"message": "Download File Request Failed"}}

    def test_delete_failure_UNICODEDECODEERROR(self, setup_test_client):
        test_client: TestClient
        file: PosixPath
        test_client, file = setup_test_client
        file_id = file.name
        fake_file_info = FileInformationFactory.create(file_id=file_id, location=file)

        with patch(
            "app.services.file_service.get_file_info",
            MagicMock(side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "pytest")),
        ):
            response = test_client.get(url=f"/download/{file_id}")

        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail": {"message": "Download File Request Failed"}}

    def test_delete_failure_EXCEPTION(self, setup_test_client):
        test_client: TestClient
        file: PosixPath
        test_client, file = setup_test_client
        file_id = file.name
        fake_file_info = FileInformationFactory.create(file_id=file_id, location=file)

        with patch(
            "app.services.file_service.get_file_info",
            MagicMock(side_effect=Exception),
        ):
            response = test_client.get(url=f"/download/{file_id}")

        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail": {"message": "Download File Request Failed"}}
