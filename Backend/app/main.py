from fastapi import FastAPI
from fastapi,middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(
    title = "Aegis-SRE Sentinal API",
    description="Proactive log monitoring powered by Machine Learning.",
    version="1.0.0"
)