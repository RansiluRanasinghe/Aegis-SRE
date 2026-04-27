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

        prompt =  f"""You are Aegis, a strict Site Reliability Engineer. Analyze this anomaly.

[CRITICAL ANOMALY LOG]
Status Code: {anomaly_log['status']}
Payload Size: {anomaly_log['bytes']} bytes
Request Frequency: {anomaly_log['ip_freq']}

[SRE PLAYBOOK RULES - APPLY EXACTLY ONE MATCHING RULE]
RULE 1: IF Status Code is 401 or 403 -> Diagnosis: Brute Force / Scanner. Mitigation: Use `fail2ban` or block IP.
RULE 2: IF Payload Size > 1000000 bytes -> Diagnosis: Data Exfiltration. Mitigation: Terminate active sessions and rotate API keys.
RULE 3: IF Status Code is 500 or 503 -> Diagnosis: Application Crash/Backend Failure. Mitigation: Restart service and check stack trace.
RULE 4: IF Request Frequency > 500 AND Payload Size > 1000 -> Diagnosis: Volumetric DDoS. Mitigation: Execute `iptables -A INPUT -s <IP> -j DROP`.

[TASK]
Based on the numbers in the CRITICAL ANOMALY LOG, identify which RULE applies. 
Write a 2-sentence response stating the exact diagnosis and the required mitigation. Do not invent new details."""   
        
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