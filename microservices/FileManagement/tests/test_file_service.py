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
