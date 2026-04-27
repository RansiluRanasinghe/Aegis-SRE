import os

class Settings:

    PROJECT_NAME:str = "Aegis-SRE Sentinel API"
    PROJECT_VERSION:str = "1.0.0" 

    OLLAMA_HOST:str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_API_URL:str = f"{OLLAMA_HOST}/api/generate"
    LLM_MODEL:str = os.getenv("LLM_MODEL", "llama3.2:1b")

    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 200

    