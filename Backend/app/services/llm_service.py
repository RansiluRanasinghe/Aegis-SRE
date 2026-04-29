import requests
from app.core.config import settings
from app.core.rule_engine import evaluate_anomaly

class AegisLLMService:

    def __init__(self):
        self.api_url = settings.OLLAMA_API_URL
        self.model = settings.LLM_MODEL

        print(f"Aegis-SRE: GenAI Engine initialized. Target: {self.api_url} ({self.model})")

    def diagnose(self, anomaly_log: dict, context_logs: list[dict]) -> str:

        print("Aegis-Brain: Crafting Root Cause Analysis...")

        status = anomaly_log["status"]
        bytes_size = anomaly_log["bytes"]
        ip_freq = anomaly_log["ip_freq"]

        system_diagnosis = evaluate_anomaly(status, bytes_size, ip_freq)

        prompt = f"""You are Aegis, a strict Site Reliability Engineer. 
Write a 2-sentence Incident Report for the Command Center dashboard.

[INCIDENT DATA]
Status Code: {status}
Payload Size: {bytes_size} bytes
Request Frequency: {ip_freq}

[SYSTEM ANALYSIS]
{system_diagnosis}

[TASK]
Draft a concise, highly technical summary combining the Incident Data with the System Analysis. Do not invent new facts. Be cold and precise.
"""   
        
        payload = {
            "model" : self.model,
            "prompt" : prompt,
            "stream" : False,
            "options" : {
                "temperature" : settings.LLM_TEMPERATURE,
                "num_predict" : settings.LLM_MAX_TOKENS
            }
        }

        try:

            response = requests.post(self.api_url, json=payload, timeout=45.0)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "Error: Empty response from LLM.").strip()
        
        except requests.exceptions.Timeout:
            return "DIAGNOSIS FAILED: GenAI model timed out (Exceeded 10s). Manual SRE intervention required."
        except requests.exceptions.ConnectionError:
            return "DIAGNOSIS FAILED: Cannot connect to Ollama. Ensure Llama 3.2 is running locally on port 11434."
        except Exception as e:
            return f"DIAGNOSIS FAILED: Unexpected GenAI pipeline error: {str(e)}"
        
llm_engine = AegisLLMService()        