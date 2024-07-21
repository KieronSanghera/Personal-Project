from app.dependencies import dependency
from pytest import fixture
import pytest
from unittest.mock import Mock
import redis.asyncio as redis
from fastapi import Request


class TestDependencies:
    
    @fixture()
    def mock_request(self):
        # Create a mock Redis instance
        mock_redis = Mock(spec=redis.Redis)

        # Create a mock app state with the Redis instance
        mock_app_state = Mock()
        mock_app_state.redis = mock_redis

        # Create a mock request object with the app state
        mock_request = Mock(spec=Request)
        mock_request.app.state = mock_app_state

        return mock_request, mock_redis

    @pytest.mark.asyncio
    async def test_get_redis(self, mock_request):
        request, mock_redis = mock_request
        
        # Call the function
        result = await dependency.get_redis(request)

        # Assert that the returned value is the mock Redis instance
        assert result is mock_redis
        assert isinstance(result, redis.Redis)