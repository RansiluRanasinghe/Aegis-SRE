from pydantic import BaseModel, Field
from typing import Optional

class LogFeatureInput(BaseModel):

    bytes: float = Field(
        ...,
        description="The size of the payload in bytes.",
        ge=0
    )

    status: int = Field(
        ...,
        description="The HTTP status code of the response.",
        ge=100,
        le=599
    )

    hour: int = Field(
        ...,
        description="Hour of the day the request was made (0-23).",
        ge=0,
        le=23
    )

    ip_freq: int = Field(
        ...,
        description="Frequency count of requests from this IP in the current window.",
        ge=1
    )

    is_error: int = Field(
        ...,
        description="Binary flag: 1 if status is 4xx/5xx, else 0.",
        ge=0,
        le=1
    )

    ip_address: str = Field(..., description="The source IP address of the request.")

    class Config:
        json_schema_extra = {
            "example": {
                "bytes" : 5667.0,
                "status" : 200,
                "hour" :13,
                "ip_freq" : 78,
                "is_error" : 0,
                "ip_address": "192.168.1.5"
            }
        }

class TicketRequest(BaseModel):
    title: str
    body: str   

class AnomalyResponse(BaseModel):

    is_anomaly: bool
    confidence_score: float
    message: str

    root_cause_analysis: Optional[str] = Field(
        default=None,
        description="The contextual Root Cause Analysis explaining WHY it happened."
    )

    suggested_patch: Optional[str] = Field(
        default=None,
        description="The suggested code or configuration fix."
    )

    referenced_commit: Optional[str] = Field(
        default=None,
        description="The specific git commit hash responsible for the anomaly."
    )

    reasoning_scrap: Optional[str] = Field(
        default=None,
        description="The LLM's internal chain-of-thought."
    )       