from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from collections import deque
import time
from app.schemas.log_schemas import LogFeatureInput, AnomalyResonse, TicketRequest
from app.services.ml_services import ml_engine
from app.services.llm_service import llm_engine
from app.services.github_service import create_incident_ticket

router = APIRouter()

context_buffer = deque(maxlen=5)

llm_cache = {
    "diagnosis" : None,
    "expires_at" : 0.0
}

CACHE_TTL = 10.0

telemetry_history = deque(maxlen=20)

system_state = {
    "active_incident" : None
}

@router.get("/health", summary="Health Check", description="Endpoint to check if the API is running.")
def health_check():
    return {
        "status" : "online",
        "engine" : "Aegis-SRE Isolation Forest",
        "llm_engine" : f"{llm_engine.model} configured",
        "context_buffer_size" : len(context_buffer)
    }

@router.get("/telemetry", summary="Live Telemetry Feed")
def get_telemetry():
    return {
        "logs" : list(telemetry_history),
        "active_incident" : system_state["active_incident"]
    }

@router.post("/analyze", response_model=AnomalyResonse, summary="Analyze Log & Trigger GenAI", description="Endpoint to analyze log features and determine if it's an anomaly.")
def analyze_log(log_data: LogFeatureInput):

    try:

        log_dict = log_data.model_dump()

        prediction_result = ml_engine.predict(log_dict)

        ui_log = {
            "Timestamp": time.strftime("%H:%M:%S"),
            "Status": log_dict["status"],
            "Bytes": log_dict["bytes"],
            "Freq": log_dict["ip_freq"],
            "ML Score": round(prediction_result["confidence_score"], 3),
            "Is Anomaly": "YES" if prediction_result["is_anomaly"] else "NO"
        }

        telemetry_history.append(ui_log)

        if not prediction_result["is_anomaly"]:
            context_buffer.append(log_dict)

            return AnomalyResonse(
                is_anomaly=False,
                confidence_score=prediction_result["confidence_score"],
                message="OK: Traffic within normal parameters.",
                root_cause_analysis=None,
                suggested_patch=None,
                referenced_commit=None,
                reasoning_scrap=None
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

                system_state["active_incident"] = {
                    "root_cause_analysis": final_diagnosis.get("root_cause_analysis"),
                    "suggested_patch": final_diagnosis.get("suggested_patch"),
                    "referenced_commit": final_diagnosis.get("referenced_commit"),
                    "reasoning_scrap": final_diagnosis.get("reasoning")
                }

             return AnomalyResonse(
                is_anomaly=True,
                confidence_score=prediction_result["confidence_score"],
                message="CRITICAL: Outlier behavior detected. GenAI RCA generated.",
                root_cause_analysis=final_diagnosis.get("root_cause_analysis"),
                suggested_patch=final_diagnosis.get("suggested_patch"),
                referenced_commit=final_diagnosis.get("referenced_commit"),
                reasoning_scrap=final_diagnosis.get("reasoning"),
                )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/tickets", summary="File an Approved SRE Ticket")
def create_ticket(ticket_request: TicketRequest):

    try:
        issue_url = create_incident_ticket(ticket_request.title, ticket_request.body)

        if issue_url.startswith("Error"):
            raise HTTPException(status_code=500, detail=issue_url)

        return {"status": "success", "issue_url": issue_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create ticket: {str(e)}")          