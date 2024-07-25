from .file_factory import FileInformationFactory, UploadFileFactory
from unittest.mock import patch, MagicMock
from app.services import file_service
from app.schemas.schemas import FileInformation
import os
from pathlib import PosixPath
import pytest
from pytest import fixture
import responses
import json


@fixture()
def setup_fake_files(tmp_path):
    path: PosixPath = tmp_path / "test_file"
    path.mkdir()
    file = path / "test.txt"
    file.write_text("Test file with some fake content")
    yield file


class TestFileServiceSuccess:

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
        data = file_service.get_file_info(file_id=file_id)
        assert response_file_info == data

    def test_delete_file_success(self, setup_fake_files):
        file = setup_fake_files
        fake_file_info: FileInformation = FileInformationFactory.create()
        fake_file_info.location = file
        assert os.path.isfile(fake_file_info.location)
        file_service.delete_file(fake_file_info)
        assert not os.path.isfile(fake_file_info.location)

    def test_delete_file_success_no_file(self):
        fake_file_info: FileInformation = FileInformationFactory.create()
        with patch("pathlib.PosixPath.is_file", MagicMock(return_value=False)):
            file_service.delete_file(fake_file_info)


class TestFileServiceFailure:
    
    @responses.activate
    def test_get_file_info_failed(self):
        file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        response_metadata = '{"metadata": {  "file_id": "1564fd75-fb2a-48ad-ace3-7254ae16b4b1", "filename": "surface.txt",  "filesize": "21",  "location": "/tmp" }}'
        response_dict = json.loads(response_metadata)
        response_file_info = FileInformation(**response_dict["metadata"])
        responses.add(
            method=responses.GET,
            url = f"http://localhost:80/getMetadata/{file_id}",
            status = 500,
            body = response_metadata,
        )
        with pytest.raises(Exception):
            file_service.get_file_info(file_id=file_id)


    def test_delete_file_failure_PERMISSIONERROR(self):
        fake_file_info: FileInformation = FileInformationFactory.create()
        with patch("pathlib.PosixPath.is_file", MagicMock(return_value=True)):
            with patch("pathlib.PosixPath.unlink", side_effect=PermissionError()):
                assert file_service.delete_file(fake_file_info) == False

    def test_delete_file_failure_EXCEPTION(self):
        fake_file_info: FileInformation = FileInformationFactory.create()
        with patch("pathlib.PosixPath.is_file", MagicMock(return_value=True)):
            with patch("pathlib.PosixPath.unlink", side_effect=Exception()):
                assert file_service.delete_file(fake_file_info) == False
