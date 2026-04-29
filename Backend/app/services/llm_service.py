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

        if context_logs:
            history_str = "\n".join([f"- Status: {l['status']} | Bytes: {l['bytes']} | Freq: {l['ip_freq']}" for l in context_logs])
        else:
            history_str = "No preceding logs. Sudden occurrence."      

        prompt = f"""Rewrite the telemetry into a 2-sentence SRE report. Follow the exact pattern of the examples. Do not invent details.

Example 1:
Input: Status 503, Payload 0.0 bytes. Diagnosis: Application Crash / Backend Failure.
Output: A backend application crash was detected via a 503 status code with a 0.0-byte payload. The service is being restarted and stack traces are being reviewed to restore stability.

Example 2:
Input: Status 401, Payload 120.0 bytes. Diagnosis: Brute Force / Scanner Attack. Action: Block IP via fail2ban.
Output: A brute force scanner attack was detected via anomalous 401 unauthorized requests. Immediate mitigation has been triggered to block the offending IP address via fail2ban.

Now do this one:
Input: Status {status}, Payload {bytes_size} bytes. Diagnosis: {system_diagnosis}
Output:"""
        
        payload = {
            "model" : self.model,
            "prompt" : prompt,
            "stream" : False,
            "options" : {
                "temperature" : 0.1,
                "num_predict" : 100
            }
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=45.0)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "Error: Empty response from LLM.").strip()
            
        except requests.exceptions.Timeout:
            return "DIAGNOSIS FAILED: GenAI model timed out. Manual SRE intervention required."
        except Exception as e:
            return f"DIAGNOSIS FAILED: Unexpected pipeline error: {str(e)}"
        
llm_engine = AegisLLMService()        