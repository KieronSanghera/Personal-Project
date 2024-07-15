from pytest import fixture
from fastapi.testclient import TestClient
from app.main import app

@fixture(autouse=True)
def setup_test_client():
    """Setup class fixture"""
    client: TestClient = TestClient(app)
    yield client
    
def test_basic_endpoint(setup_test_client):
    test_client: TestClient = setup_test_client
    test_client.get(url="/")