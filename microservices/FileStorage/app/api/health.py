from fastapi import APIRouter, Query
from datetime import datetime


router = APIRouter()


@router.get("/livez")
async def livez(verbose: bool = Query(False, description="Include verbose information")):
    if verbose:
        # Provide verbose information
        return {
            "status": "ok",
            "details": {
                "message": "Service is live and operational.",
                "timestamp": datetime.now()
            }
        }
    else:
        # Standard response
        return {"status": "live"}

@router.get("/readyz")
async def readyz(verbose: bool = Query(False, description="Include verbose information")):
    if verbose:
        # Provide verbose information
        return {
            "status": "ready",
            "details": {
                "message": "Service is ready to accept traffic.",
                "timestamp": datetime.now()
            }
        }
    else:
        # Standard response
        return {"status": "ready"}
    
