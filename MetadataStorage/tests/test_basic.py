from fastapi.testclient import TestClient
from app.main import app
from httpx import Response


class TestBasicFunction:

    def test_basic(self):
        client: TestClient = TestClient(app)
        response: Response = client.get(url="/")
