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

        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an automated SRE reporting script. You do not converse. You do not greet. You output ONLY the final 2-sentence executive summary. Do not invent details. Combine the anomaly data, the required mitigation, and the recent history into a clean, professional incident report.<|eot_id|><|start_header_id|>user<|end_header_id|>
[RECENT TRAFFIC HISTORY]
{history_str}

[ANOMALY TRIGGER]
Status: {status} | Payload: {bytes_size} bytes | Frequency: {ip_freq}

[REQUIRED DIAGNOSIS & MITIGATION]
{system_diagnosis}

Write the 2-sentence incident report.<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        
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