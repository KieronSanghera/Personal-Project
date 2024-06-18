from fastapi.testclient import TestClient
from pytest import fixture
from app.main import app
from httpx import Response
from pathlib import PosixPath

class TestUploadSuccess():
    """Class to test upload functionality"""
    
    @fixture(autouse=True)
    def setup_test_client(self, tmp_path):
        """Setup class fixture"""
        client: TestClient = TestClient(app)
        
        path: PosixPath = tmp_path / "test_file"
        path.mkdir()
        file = path / "test.txt"
        file.write_text("Test file with some fake content")
        yield client, file
    
    def test_successful_upload(self, setup_test_client):
        test_client, file = setup_test_client
        with open(file, "rb") as tmpfile:
            files = {"file": tmpfile}
            response: Response = test_client.post(url="/upload", files=files)
            
        assert response.status_code == 200
        print(response.json())
