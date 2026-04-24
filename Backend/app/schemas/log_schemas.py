from pydantic import BaseModel, Field

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
        description="Binary flag: 1 if status is 4xx/5xx, else 0.",
        ge=0,
        le=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "bytes" : 5667.0,
                "status" : 200,
                "hour" :13,
                "ip_freq" : 78,
                "is_error" : 0
            }
        }

class AnomalyResonse(BaseModel):

    is_anomaly: bool
    confidence_score: float
    message: str        