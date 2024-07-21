import pytest
from unittest.mock import patch, AsyncMock
from fastapi import FastAPI
import redis.exceptions
from app.main import lifespan 
import redis



@pytest.mark.asyncio
async def test_lifespan_success():
    # Create a FastAPI instance
    app = FastAPI()
    
    mocked_redis = AsyncMock()
    
    with patch("app.main.redis.Redis", AsyncMock(return_value=mocked_redis)):
        async with lifespan(app=app):
            assert app.state.redis == mocked_redis

@pytest.mark.asyncio
async def test_lifespan_error():
    app = FastAPI()
    
    mocked_redis = AsyncMock()
    
    with patch("app.main.redis.Redis", AsyncMock(return_value=mocked_redis)):
        with patch.object(mocked_redis, "ping", AsyncMock(side_effect=redis.exceptions.ConnectionError())):
            async with lifespan(app=app):
                with pytest.raises(AttributeError):
                    app.state.redis == mocked_redis
    
