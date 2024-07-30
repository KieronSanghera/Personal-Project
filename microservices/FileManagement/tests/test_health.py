from app.main import app
from fastapi.testclient import TestClient
from pytest import fixture
import json
from freezegun import freeze_time


@fixture(autouse=True)
def setup_test_client():
    """Setup class fixture"""
    client: TestClient = TestClient(app)
    yield client
    
class TestHealth:
    
    def test_livez(self, setup_test_client):
        test_client: TestClient = setup_test_client
        response = test_client.get("/livez")
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 200
        assert content == {"status": "live"}
    
    def test_readyz(self, setup_test_client):
        test_client: TestClient = setup_test_client
        response = test_client.get("/readyz")
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 200
        assert content == {"status": "ready"}
        
    @freeze_time("2000-01-01 12:00:00")
    def test_livez_verbose(self, setup_test_client):
        test_client: TestClient = setup_test_client
        response = test_client.get("/livez?verbose=true")
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 200
        assert content == {
            "status": "ok",
            "details": {
                "message": "Service is live and operational.",
                "timestamp": "2000-01-01T12:00:00",
            },
        }

    @freeze_time("2000-01-01 12:00:00")
    def test_readyz_verbose(self, setup_test_client):
        test_client: TestClient = setup_test_client
        response = test_client.get("/readyz?verbose=true")
        content = json.loads(response.content.decode("utf-8"))
        assert response.status_code == 200
        assert content == {
            "status": "ready",
            "details": {
                "message": "Service is ready to accept traffic.",
                "timestamp": "2000-01-01T12:00:00",
            },
        }

        