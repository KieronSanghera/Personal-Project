from app.config import configs
import redis.asyncio as redis

class RedisException(Exception):
    """Custom Exception for Metadata Storage redis services"""
    
    def __init__(self, message):
        self.message = message
        super().__init__(message)
        
    @classmethod
    async def redis_check(cls, message):
        try:
            redis_client = redis.Redis(host=configs.redis_hostname, port=6379, db=0)

            await redis_client.ping()
            await redis_client.aclose()
            is_redis_connected = True
        except redis.ConnectionError:
            await redis_client.aclose()
            is_redis_connected = False
        message = f"{message} | Redis Connected: {is_redis_connected}"
        
        return cls(message)
            