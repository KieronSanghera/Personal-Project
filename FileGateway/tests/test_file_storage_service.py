from app.services.file_storage_service import store_file
from unittest.mock import patch, MagicMock


class MockedResponse:
    def __init__(self, content):
        self.content = content

def test_store_file():
    mock_response = MockedResponse(content=b"yay")
    with patch("requests.post", MagicMock(return_value=mock_response)):
        response = store_file({},{})
        assert response == mock_response