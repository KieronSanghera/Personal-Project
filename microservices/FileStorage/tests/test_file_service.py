from .file_factory import FileInformationFactory, UploadFileFactory
from unittest.mock import patch, MagicMock
from app.services import file_service
from app.schemas.schemas import FileInformation
import os
from pathlib import PosixPath
import pytest
from pytest import fixture


@fixture()
def setup_fake_files(tmp_path):
    path: PosixPath = tmp_path / "test_file"
    path.mkdir()
    file = path / "test.txt"
    file.write_text("Test file with some fake content")
    yield file


class TestFileServiceSuccess:

    def test_store_file_success(self, tmpdir):
        fake_file = UploadFileFactory.create()
        with patch("app.schemas.schemas.configs.store_dir", tmpdir):
            fake_file_info: FileInformation = FileInformationFactory.create()
        file_service.store_file(file=fake_file, file_info=fake_file_info)
        assert os.path.isfile(fake_file_info.location)

    def test_failed_file_success(self, setup_fake_files):
        file = setup_fake_files
        assert os.path.isfile(file)
        file_service.failed_file(file)
        assert not os.path.isfile(file)

    def test_failed_file_success(self):
        with patch("pathlib.PosixPath.is_file", MagicMock(return_value=False)):
            file_service.failed_file(PosixPath("/tmp"))


class TestFileServiceFailure:

    @patch("shutil.copyfileobj", MagicMock(side_effect=IOError()))
    def test_store_file_failure_IOERROR(self, tmpdir):
        fake_file = UploadFileFactory.create()
        with patch("app.schemas.schemas.configs.store_dir", tmpdir):
            fake_file_info = FileInformationFactory.create()

        with pytest.raises(IOError):
                file_service.store_file(file=fake_file, file_info=fake_file_info)

        assert os.path.isfile(fake_file_info.location)

    @patch("shutil.copyfileobj", MagicMock(side_effect=TypeError()))
    def test_store_file_failure_TYPEERROR(self, tmpdir):
        fake_file = UploadFileFactory.create()
        with patch("app.schemas.schemas.configs.store_dir", tmpdir):
            fake_file_info = FileInformationFactory.create()

        with pytest.raises(TypeError):
            file_service.store_file(file=fake_file, file_info=fake_file_info)

        assert os.path.isfile(fake_file_info.location)

    @patch("shutil.copyfileobj", MagicMock(side_effect=MemoryError()))
    def test_store_file_failure_MEMORYERROR(self, tmpdir):
        fake_file = UploadFileFactory.create()
        with patch("app.schemas.schemas.configs.store_dir", tmpdir):
            fake_file_info = FileInformationFactory.create()

        with pytest.raises(MemoryError):
            file_service.store_file(file=fake_file, file_info=fake_file_info)

        assert os.path.isfile(fake_file_info.location)

    @patch("shutil.copyfileobj", MagicMock(side_effect=Exception()))
    def test_store_file_failure_EXCEPTION(self, tmpdir):
        fake_file = UploadFileFactory.create()
        with patch("app.schemas.schemas.configs.store_dir", tmpdir):
            fake_file_info = FileInformationFactory.create()
            
        with pytest.raises(Exception):
                file_service.store_file(file=fake_file, file_info=fake_file_info)

        assert os.path.isfile(fake_file_info.location)

    def test_failed_file_failure_PERMISSIONERROR(self):
        with patch("pathlib.PosixPath.is_file", MagicMock(return_value=True)):
            with patch("pathlib.PosixPath.unlink", side_effect=PermissionError()):
                assert file_service.failed_file(PosixPath("/tmp")) == False

    def test_failed_file_failure_EXCEPTION(self):
        with patch("pathlib.PosixPath.is_file", MagicMock(return_value=True)):
            with patch("pathlib.PosixPath.unlink", side_effect=Exception()):
                assert file_service.failed_file(PosixPath("/tmp")) == False
