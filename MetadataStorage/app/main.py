from fastapi import FastAPI
from app.api.endpoints import router as endpoint_router
from app.api.health import router as health_router
from app.config import configs
from contextlib import asynccontextmanager
import redis.asyncio as redis
from redis import exceptions as redisExceptions
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = await redis.Redis(
        host=configs.redis_hostname, port=configs.redis_port, db=0
    )
    # Implement a timeout
    try:
        await redis_client.ping()
        logging.info("Redis Connection Successful")
        app.state.redis = redis_client
        # TODO: Make ready check True
    except redisExceptions.ConnectionError as error:
        logging.error("Redis Connection Failed")
        # TODO: Make ready check False
    yield
    await redis_client.aclose()


app = FastAPI(debug=configs.is_debug, lifespan=lifespan)
app.include_router(endpoint_router)
app.include_router(health_router)
