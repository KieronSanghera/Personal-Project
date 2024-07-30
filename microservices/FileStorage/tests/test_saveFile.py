from fastapi.testclient import TestClient
from pytest import fixture
from app.main import app
from app.api import endpoints
from httpx import Response
from pathlib import PosixPath
from uuid import uuid4
from file_factory import FileInformationFactory
from unittest.mock import patch, MagicMock


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

    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=True))
    def test_successful_saveFile(self, setup_test_client, tmpdir):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        
        with patch("app.schemas.schemas.configs.store_dir", tmpdir):
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
    
    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=False))
    def test_saveFile_failure_metadata_storage(self, setup_test_client, tmpdir):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        
        with patch("app.schemas.schemas.configs.store_dir", tmpdir):
            with open(file, "rb") as tmpfile:
                files = {"file": tmpfile}
                response: Response = test_client.post(
                    url="/saveFile",
                    data=file_data,
                    files=files,
                )

        assert response.status_code == 500

    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=True))
    @patch("shutil.copyfileobj", MagicMock(side_effect=IOError()))
    def test_saveFile_store_file_failure_IOERROR(self, setup_test_client):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        with open(file, "rb") as tmpfile:
            files = {"file": tmpfile}
            response: Response = test_client.post(
                url="/saveFile",
                data=file_data,
                files=files,
            )

        print(response.content)
        assert response.status_code == 500

    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=True))
    @patch("shutil.copyfileobj", MagicMock(side_effect=TypeError()))
    def test_saveFile_store_file_failure_TYPEERROR(self, setup_test_client):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        with open(file, "rb") as tmpfile:
            files = {"file": tmpfile}
            response: Response = test_client.post(
                url="/saveFile",
                data=file_data,
                files=files,
            )

        assert response.status_code == 500

    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=True))
    @patch("shutil.copyfileobj", MagicMock(side_effect=MemoryError()))
    def test_saveFile_store_file_failure_MEMORYERROR(self, setup_test_client):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        with open(file, "rb") as tmpfile:
            files = {"file": tmpfile}
            response: Response = test_client.post(
                url="/saveFile",
                data=file_data,
                files=files,
            )

        assert response.status_code == 500

    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=True))
    @patch("shutil.copyfileobj", MagicMock(side_effect=Exception()))
    def test_saveFile_store_file_failure_EXCEPTION(self, setup_test_client):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        with open(file, "rb") as tmpfile:
            files = {"file": tmpfile}
            response: Response = test_client.post(
                url="/saveFile",
                data=file_data,
                files=files,
            )

        assert response.status_code == 500

    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=True))
    @patch("shutil.copyfileobj", MagicMock(side_effect=Exception()))
    @patch(
        "app.services.file_service.PosixPath.unlink", MagicMock(side_effect=Exception())
    )
    def test_saveFile_store_file_failure_unlink_EXCEPTION(
        self, setup_test_client, tmpdir
    ):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        with patch.object(
            PosixPath,
            "resolve",
            MagicMock(
                return_value=PosixPath(f"{tmpdir}/{file_data['file_id']}").resolve()
            ),
        ):
            with open(file, "rb") as tmpfile:
                files = {"file": tmpfile}
                response: Response = test_client.post(
                    url="/saveFile",
                    data=file_data,
                    files=files,
                )

        assert response.status_code == 500

    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=True))
    @patch("shutil.copyfileobj", MagicMock(side_effect=Exception()))
    @patch(
        "app.services.file_service.PosixPath.unlink",
        MagicMock(side_effect=PermissionError()),
    )
    def test_saveFile_store_file_failure_unlink_PERMISSIONERROR(
        self, setup_test_client, tmpdir
    ):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        with patch.object(
            PosixPath,
            "resolve",
            MagicMock(
                return_value=PosixPath(f"{tmpdir}/{file_data['file_id']}").resolve()
            ),
        ):
            with open(file, "rb") as tmpfile:
                files = {"file": tmpfile}
                response: Response = test_client.post(
                    url="/saveFile",
                    data=file_data,
                    files=files,
                )

        assert response.status_code == 500

    @patch("app.services.metadata_service.new_metadata_request", MagicMock(return_value=True))
    @patch("shutil.copyfileobj", MagicMock(side_effect=Exception()))
    @patch(
        "app.services.file_service.PosixPath.unlink",
        MagicMock(side_effect=FileNotFoundError()),
    )
    def test_saveFile_store_file_failure_unlink_FILENOTFOUNDERROR(
        self, setup_test_client, tmpdir
    ):
        test_client, file = setup_test_client
        file_data = FileInformationFactory.create_dict()
        with patch.object(
            PosixPath,
            "resolve",
            MagicMock(
                return_value=PosixPath(f"{tmpdir}/{file_data['file_id']}").resolve()
            ),
        ):
            with open(file, "rb") as tmpfile:
                files = {"file": tmpfile}
                response: Response = test_client.post(
                    url="/saveFile",
                    data=file_data,
                    files=files,
                )

        assert response.status_code == 500
