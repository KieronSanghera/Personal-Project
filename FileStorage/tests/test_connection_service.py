from app.services import connection_service
from app.schemas.schemas import ConnectionInformation
from unittest.mock import patch, MagicMock
import pytest
from .request_factory import RequestFactory
from uuid import UUID
from ipaddress import IPv4Address


@pytest.fixture(autouse=True)
def mock_socket():
    with patch("socket.socket") as mock_socket:
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        yield mock_socket_instance


class TestConnectionServiceSuccess:
    """Class to test connection services success"""

    @patch(
        "app.services.connection_service.get_host_ip",
        MagicMock(return_value="127.0.0.1"),
    )
    def test_connection_information(self):
        mock_request = RequestFactory.create()
        test_info = connection_service.connection_info(mock_request)

        assert isinstance(test_info, ConnectionInformation)
        assert isinstance(test_info.connection_id, UUID)
        assert test_info.source_addr == "testclient"
        assert isinstance(test_info.host_addr, IPv4Address)
        assert test_info.host_addr == IPv4Address("127.0.0.1")

    def test_get_host_ip(self, mock_socket):
        """Success path of get host ip"""
        mock_socket.getsockname.return_value = ("192.168.1.1", 0)

        host_ip = connection_service.get_host_ip()
        assert host_ip == "192.168.1.1"

        mock_socket.connect.assert_called_once_with(("8.8.8.8", 80))
        mock_socket.close.assert_called_once()


class TestConnectionServiceFailure:
    """Class to test connection services failure"""

    def test_get_host_ip_exception(self, mock_socket):
        """Test exception path of get host ip"""
        mock_socket.connect.side_effect = Exception("Test exception")

        ip = connection_service.get_host_ip()
        assert ip == "Unable to get IP address"

        mock_socket.connect.assert_called_once_with(("8.8.8.8", 80))
        mock_socket.close.assert_not_called()
