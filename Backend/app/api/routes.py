from fastapi import APIRouter, HTTPException
from app.schemas.log_schemas import LogFeatureInput, AnomalyResonse
from app.services.ml_services import ml_engine

router = APIRouter()

@router.get("/health", summary="Health Check", description="Endpoint to check if the API is running.")
async def health_check():
    return {
        "status" : "online",
        "engine" : "Aegis-SRE Isolation Forest",
        "ready" : ml_engine.model is not None
    }