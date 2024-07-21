from fastapi import FastAPI
from app.api.endpoints import router as endpoint_router
from app.api.health import router as health_router
from app.config import configs

app = FastAPI(debug=configs.is_debug)
app.include_router(endpoint_router)
app.include_router(health_router)
