from app.services import redis_service
from app.exceptions.redis_exceptions import RedisException
from file_factory import FileInformationFactory
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
import redis
from pydantic import ValidationError
from uuid import uuid4


class TestRedisServiceSuccess:
    
    @pytest.mark.asyncio
    @patch.object(redis.asyncio.Redis, "hset", AsyncMock(return_value=1))
    async def test_new_metadata(self):
        file_info = FileInformationFactory.create()
        response = await redis_service.new_metadata(file_data=file_info, redis_connection=redis.asyncio.Redis)
        assert response is True
        
    @pytest.mark.asyncio
    @patch.object(redis.asyncio.Redis, "hset", AsyncMock(return_value=0))
    @patch.object(redis.asyncio.Redis, "exists", AsyncMock(return_value=True))
    async def test_new_metadata_existing(self):
        file_info = FileInformationFactory.create()
        response = await redis_service.new_metadata(file_data=file_info, redis_connection=redis.asyncio.Redis)
        assert response is True
        
    @pytest.mark.asyncio
    async def test_get_metadata(self):
        file_info = FileInformationFactory.create()
        mock_redis_response = str(file_info.model_dump_database()).encode()
        
        
        with patch.object(redis.asyncio.Redis, "hget", AsyncMock(return_value=mock_redis_response)):
            response = await redis_service.get_metadata(file_info.file_id, redis_connection=redis.asyncio.Redis)
        
        response == file_info

    @pytest.mark.asyncio
    @patch.object(redis.asyncio.Redis, "hdel", AsyncMock(return_value=1))
    @patch.object(redis.asyncio.Redis, "hkeys", AsyncMock(return_value="2"))
    async def test_delete_metadata(self):
        response = await redis_service.delete_metadata(file_id=uuid4(), redis_connection=redis.asyncio.Redis)
        assert response is True
        
    @pytest.mark.asyncio
    @patch.object(redis.asyncio.Redis, "hdel", AsyncMock(return_value=0))
    @patch.object(redis.asyncio.Redis, "hkeys", AsyncMock(return_value="2"))
    @patch.object(redis.asyncio.Redis, "exists", AsyncMock(return_value=False))
    async def test_delete_metadata_not_exists(self):
        response = await redis_service.delete_metadata(file_id=uuid4(), redis_connection=redis.asyncio.Redis)
        assert response is True
    
        
class TestRedisServiceFailure:
    
    @pytest.mark.asyncio
    @patch.object(redis.asyncio.Redis, "hset", AsyncMock(return_value=0))
    @patch.object(redis.asyncio.Redis, "exists", AsyncMock(return_value=False))
    async def test_new_metadata_existing_failure(self):
        file_info = FileInformationFactory.create()
        response = await redis_service.new_metadata(file_data=file_info, redis_connection=redis.asyncio.Redis)
        assert response is False
    
    @pytest.mark.asyncio
    async def test_get_metadata_does_not_exist(self):
        file_info = FileInformationFactory.create()
        
        with pytest.raises(RedisException):
            with patch.object(redis.asyncio.Redis, "hget", AsyncMock(return_value=None)):
                await redis_service.get_metadata(file_info.file_id, redis_connection=redis.asyncio.Redis)
                
    @pytest.mark.asyncio
    async def test_get_metadata_non_schema_match(self):
        file_info = FileInformationFactory.create()
        mock_redis_response = str(file_info.model_dump_database()).encode()
        
        with pytest.raises(ValidationError):
            with patch.object(redis.asyncio.Redis, "hget", AsyncMock(return_value=mock_redis_response)):
                with patch("app.services.redis_service.json.loads", MagicMock(return_value={})):
                    response = await redis_service.get_metadata(file_info.file_id, redis_connection=redis.asyncio.Redis)
        
    @pytest.mark.asyncio
    @patch.object(redis.asyncio.Redis, "hdel", AsyncMock(return_value=0))
    @patch.object(redis.asyncio.Redis, "hkeys", AsyncMock(return_value="2"))
    @patch.object(redis.asyncio.Redis, "exists", AsyncMock(return_value=True))
    async def test_delete_metadata_exits(self):
        response = await redis_service.delete_metadata(file_id=uuid4(), redis_connection=redis.asyncio.Redis)
        assert response is False
        