from fastapi import APIRouter, HTTPException
from app.schemas.log_schemas import LogFeatureInput, AnomalyResonse
from app.services.ml_services import ml_engine

router = APIRouter()