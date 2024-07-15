from fastapi import APIRouter, Query


router = APIRouter()


@router.get("/livez")
async def livez(verbose: bool = Query(False, description="Include verbose information")):
    if verbose:
        # Provide verbose information
        return {
            "status": "ok",
            "details": {
                "message": "Service is live and operational.",
                "timestamp": "2024-07-15T12:00:00Z"
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
                "timestamp": "2024-07-15T12:00:00Z"
            }
        }
    else:
        # Standard response
        return {"status": "ready"}
    
