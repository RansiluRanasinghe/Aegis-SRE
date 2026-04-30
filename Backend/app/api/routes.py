from fastapi import APIRouter, HTTPException
from collections import deque
import time
from app.schemas.log_schemas import LogFeatureInput, AnomalyResonse
from app.services.ml_services import ml_engine
from app.services.llm_service import llm_engine

router = APIRouter()

context_buffer = deque(maxlen=5)

llm_cache = {
    "diagnosis" : None,
    "expires_at" : 0.0
}

CACHE_TTL = 10.0

@router.get("/health", summary="Health Check", description="Endpoint to check if the API is running.")
async def health_check():
    return {
        "status" : "online",
        "engine" : "Aegis-SRE Isolation Forest",
        "llm_engine" : f"{llm_engine.model} configured",
        "context_buffer_size" : len(context_buffer)
    }

@router.post("/analyze", response_model=AnomalyResonse, summary="Analyze Log & Trigger GenAI", description="Endpoint to analyze log features and determine if it's an anomaly.")
async def analyze_log(log_data: LogFeatureInput):

    try:

        log_dict = log_data.model_dump()

        prediction_result = ml_engine.predict(log_dict)

        if not prediction_result["is_anomaly"]:
            context_buffer.append(log_dict)

            return AnomalyResonse(
                is_anomaly=False,
                confidence_score=prediction_result["confidence_score"],
                message="OK: Traffic within normal parameters.",
                llm_diagnosis=None
            )

        else:
             
             current_time = time.time()

             if current_time < llm_cache["expires_at"]:
                print("CIRCUIT BREAKER ACTIVE: Serving cached RCA. (Protecting local LLM)")
                final_diagnosis = llm_cache["diagnosis"]

             else:
                print("CIRCUIT BREAKER OPEN: Waking GenAI for new RCA...")
                final_diagnosis = llm_engine.diagnose(
                  anomaly_log =  log_dict,
                  context_logs = list(context_buffer)
                )
                llm_cache["diagnosis"] = final_diagnosis
                llm_cache["expires_at"] = current_time + CACHE_TTL

                context_buffer.clear()

             return AnomalyResonse(
                is_anomaly=True,
                confidence_score=prediction_result["confidence_score"],
                message="CRITICAL: Outlier behavior detected. GenAI RCA generated.",
                llm_diagnosis=final_diagnosis
                )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")       