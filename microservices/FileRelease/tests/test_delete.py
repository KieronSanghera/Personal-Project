from fastapi.testclient import TestClient
from pytest import fixture
from app.main import app
from uuid import uuid4
from file_factory import FileInformationFactory
from unittest.mock import patch, MagicMock
import requests
import json


@fixture(autouse=True)
def setup_test_client():
    """Setup class fixture"""
    client: TestClient = TestClient(app)
    yield client
    
class TestDeleteSuccess:
    
    def test_delete_success(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        fake_file_info = FileInformationFactory.create(file_id=fake_file_id)
        
        with patch("app.services.file_service.get_file_info", MagicMock(return_value=fake_file_info)):
            response = test_client.delete(
                url=f"/delete/{fake_file_id}"
            )
        assert response.status_code == 200
        assert response.content.decode("utf-8") == "File Successfully Deleted"
        
class TestDeleteFailure:
    
    def test_delete_failure_delete_failed(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        fake_file_info = FileInformationFactory.create(file_id=fake_file_id)
        
        with patch("app.services.file_service.get_file_info", MagicMock(return_value=fake_file_info)):
            with patch("app.services.file_service.delete_file", MagicMock(return_value=False)):
                response = test_client.delete(
                    url=f"/delete/{fake_file_id}"
                )
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail":{"message":"Delete File Request Failed"}}
        

    def test_delete_failure_CONNECTIONERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        
        with patch("app.services.file_service.get_file_info", MagicMock(side_effect=requests.exceptions.ConnectionError)):
            response = test_client.delete(
                url=f"/delete/{fake_file_id}"
            )
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail":{"message":"Delete File Request Failed"}}

    def test_delete_failure_TIMEOUT(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        
        with patch("app.services.file_service.get_file_info", MagicMock(side_effect=requests.exceptions.Timeout)):
            response = test_client.delete(
                url=f"/delete/{fake_file_id}"
            )
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail":{"message":"Delete File Request Failed"}}

    def test_delete_failure_HTTPERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        
        with patch("app.services.file_service.get_file_info", MagicMock(side_effect=requests.exceptions.HTTPError)):
            response = test_client.delete(
                url=f"/delete/{fake_file_id}"
            )
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail":{"message":"Delete File Request Failed"}}

    def test_delete_failure_REQUESTEXCEPTION(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        
        with patch("app.services.file_service.get_file_info", MagicMock(side_effect=requests.exceptions.RequestException)):
            response = test_client.delete(
                url=f"/delete/{fake_file_id}"
            )
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail":{"message":"Delete File Request Failed"}}

    def test_delete_failure_JSONDECODEERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        
        with patch("app.services.file_service.get_file_info", MagicMock(side_effect=json.JSONDecodeError("", "", 0))):
            response = test_client.delete(
                url=f"/delete/{fake_file_id}"
            )
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail":{"message":"Delete File Request Failed"}}

    def test_delete_failure_UNICODEDECODEERROR(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        
        with patch("app.services.file_service.get_file_info", MagicMock(side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "pytest"))):
            response = test_client.delete(
                url=f"/delete/{fake_file_id}"
            )
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail":{"message":"Delete File Request Failed"}}

    def test_delete_failure_EXCEPTION(self, setup_test_client):
        test_client: TestClient = setup_test_client
        fake_file_id = "259744af-8583-438e-b4ef-045e7f656a4b"
        
        with patch("app.services.file_service.get_file_info", MagicMock(side_effect=Exception)):
            response = test_client.delete(
                url=f"/delete/{fake_file_id}"
            )
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 500
        assert content == {"detail":{"message":"Delete File Request Failed"}}
