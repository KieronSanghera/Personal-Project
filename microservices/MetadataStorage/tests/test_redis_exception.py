from app.exceptions.redis_exceptions import RedisException
from unittest.mock import patch, MagicMock, AsyncMock
import redis.asyncio as redis
import pytest


class TestRedisException:

    @pytest.mark.asyncio
    @patch.object(redis.Redis, "ping", AsyncMock(return_value=""))
    async def test_redis_exception_with_connection(self):
        exception = await RedisException.redis_check("Raised for pytest")

        assert exception.message == "Raised for pytest | Redis Connected: True"

    @pytest.mark.asyncio
    @patch.object(redis.Redis, "ping", MagicMock(side_effect=redis.ConnectionError))
    async def test_redis_exception_without_connection(self):
        exception = await RedisException.redis_check("Raised for pytest")

        assert exception.message == "Raised for pytest | Redis Connected: False"
