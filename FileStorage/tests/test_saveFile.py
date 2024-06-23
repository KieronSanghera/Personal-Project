from fastapi.testclient import TestClient
from pytest import fixture
from app.main import app
from app.api import endpoints
from httpx import Response
from pathlib import PosixPath
from uuid import uuid4
from file_factory import FileFactory
from unittest import mock


@fixture(autouse=True)
def setup_test_client(tmp_path):
    """Setup class fixture"""
    client: TestClient = TestClient(app)

    path: PosixPath = tmp_path / "test_file"
    path.mkdir()
    file = path / "test.txt"
    file.write_text("Test file with some fake content")
    yield client, file


class TestSaveFileSuccess:
    """Class to test save file functionality"""

    def test_successful_saveFile(self, setup_test_client):
        test_client, file = setup_test_client
        file_data = FileFactory.create()
        with open(file, "rb") as tmpfile:
            files = {"file": tmpfile}
            response: Response = test_client.post(
                url="/saveFile",
                data=file_data,
                files=files,
            )

        assert response.status_code == 201


class TestSaveFileFailure:
    """Class to test save file functionality failure"""

    @mock.patch("shutil.copyfileobj", mock.MagicMock(side_effect=IOError()))
    def test_store_file_failure(self, setup_test_client):
        test_client, file = setup_test_client
        file_data = FileFactory.create()
        with open(file, "rb") as tmpfile:
            files = {"file": tmpfile}
            response: Response = test_client.post(
                url="/saveFile",
                data=file_data,
                files=files,
            )

        assert response.status_code == 500