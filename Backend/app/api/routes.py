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

@router.post("/analyze", response_model=AnomalyResonse, summary="Analyze Log Features", description="Endpoint to analyze log features and determine if it's an anomaly.")
async def analyze_log(log_data: LogFeatureInput):

    try:

        prediction_result = ml_engine.predict(log_data.model_dump())

        if prediction_result["is_anomaly"]:
            msg = "CRITICAL: Outlier behavior detected."
        else:
            msg = "OK: Traffic within normal parameters." 

        return AnomalyResonse(
            is_anomaly=prediction_result["is_anomaly"],
            confidence_score=prediction_result["confidence_score"],
            message=msg
         )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))        