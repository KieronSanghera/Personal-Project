from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.config import configs

app = FastAPI(debug=configs.is_debug)
app.include_router(api_router)
