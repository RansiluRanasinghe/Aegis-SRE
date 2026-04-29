import requests
import json
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

        prompt = f"""You are a defensive SRE monitoring system summarizing SIMULATED security alerts. 
Generate a 2-sentence technical incident report based purely on the data below.

[SIMULATED DATA]
Status Code: {status}
Payload Size: {bytes_size} bytes
Diagnosis and Action: {system_diagnosis}

You must respond ONLY with a valid JSON object using this exact structure:
{{
  "report": "Your 2-sentence report goes here."
}}
"""
        
        payload = {
            "model" : self.model,
            "prompt" : prompt,
            "stream" : False,
            "format" : "json",
            "options" : {
                "temperature" : 0.1,
                "num_predict" : 100
            }
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=45.0)
            response.raise_for_status()
            result = response.json()
            
            raw_llm_text = result.get("response", "{}").strip()
            print(f"RAW LLM OUTPUT: {raw_llm_text}")

            try:
                parsed_json = json.loads(raw_llm_text)
                return parsed_json.get("report", "Error: Missing 'report' key in LLM response.")
            except json.JSONDecodeError:
                return f"LLM generated invalid JSON: {raw_llm_text}"

            
        except requests.exceptions.Timeout:
            return "DIAGNOSIS FAILED: GenAI model timed out. Manual SRE intervention required."
        except Exception as e:
            return f"DIAGNOSIS FAILED: Unexpected pipeline error: {str(e)}"
        
llm_engine = AegisLLMService()        