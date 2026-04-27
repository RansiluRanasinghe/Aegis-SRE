import requests
from app.core.config import settings

class AegisLLMService:

    def __init__(self):
        self.api_url = settings.OLLAMA_API_URL
        self.model = settings.LLM_MODEL

        print(f"Aegis-SRE: GenAI Engine initialized. Target: {self.api_url} ({self.model})")

    def diagnose(self, anomaly_log: dict, context_logs: list[dict]) -> str:

        print("Aegis-Brain: Crafting Root Cause Analysis...")

        context_str = "\n".join([
            f"- Status: {log['status']} | Bytes: {log['bytes']} | IP Freq: {log['ip_freq']}" 
            for log in context_logs
        ])

        prompt =  f"""You are Aegis, an expert DevOps Site Reliability Engineer (SRE).
        Your ML Sentinel has just flagged a critical anomaly in the server logs.

        [RECENT NORMAL TRAFFIC]
        {context_str if context_str else "No recent context available. Server just booted."}

        [CRITICAL ANOMALY LOG]
        Status Code: {anomaly_log['status']}
        Payload Size (Bytes): {anomaly_log['bytes']}
        Requests from this IP: {anomaly_log['ip_freq']}

        [TASK]
        Based purely on the data above:
        1. Identify the likely technical root cause of this anomaly (e.g., DDoS, memory leak, broken endpoint, scanner bot).
        2. Suggest one specific, actionable terminal command or engineering step to mitigate it.

        [CONSTRAINTS]
        Keep your answer under 3 sentences. Be highly technical, cold, and precise. Do not use pleasantries. Do not guess beyond the provided data.
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