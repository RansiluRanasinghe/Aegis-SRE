import requests
import json
import os
from pathlib import Path
from app.core.config import settings
from app.core.rule_engine import evaluate_anomaly
from app.services.github_service import get_recent_commits

class AegisLLMService:

    def __init__(self):
        self.api_url = settings.OLLAMA_API_URL
        self.model = settings.LLM_MODEL

        print(f"Aegis-SRE: GenAI Engine initialized. Target: {self.api_url} ({self.model})")

    def _get_repo_context(self, system_diagnosis: str) -> str:

        print("Scanning live GitHub repository for culprit commits...")

        live_context = get_recent_commits(limit=15)

        return live_context


    def diagnose(self, anomaly_log: dict, context_logs: list[dict]) -> dict:

        print("Aegis-Brain: Crafting Root Cause Analysis and Code Patch...")

        status = anomaly_log["status"]
        bytes_size = anomaly_log["bytes"]
        ip_freq = anomaly_log["ip_freq"]

        system_diagnosis = evaluate_anomaly(status, bytes_size, ip_freq)

        if context_logs:
            history_str = "\n".join([f"- Status: {l['status']} | Bytes: {l['bytes']} | Freq: {l['ip_freq']}" for l in context_logs])
        else:
            history_str = "No preceding logs. Sudden occurrence."

        system_context = self._get_repo_context(system_diagnosis=system_diagnosis)          

        print(f"\n--- DEBUG: LOADED CONTEXT ---\n{system_context}\n-----------------------------\n")

        prompt = f"""You are Aegis-Brain, an elite Site Reliability Engineering AI.
You will be provided with an anomaly log and the most recent GitHub commits.

CRITICAL INSTRUCTIONS:
1. Evaluate the anomaly symptoms.
2. Review the GitHub commits to see if they caused the issue.
3. DO NOT FORCE A MATCH. If the recent commits (e.g., UI updates, README changes) are clearly unrelated to a severe backend anomaly (like a Cache Crash or Brute Force), you MUST set "referenced_commit" to "None".
4. If no commit is to blame, provide a general, high-level SRE diagnosis and suggested patch for the anomaly type.

Respond strictly in valid JSON format matching this schema:
{{
  "reasoning": "Brief internal thought process",
  "root_cause_analysis": "Detailed explanation of the failure.",
  "suggested_patch": "Actionable fix or mitigation strategy.",
  "referenced_commit": "The exact commit hash (e.g., [4193d53]) OR 'None' if no commit is related."
}}
"""
        
        payload = {
            "model" : self.model,
            "prompt" : prompt,
            "stream" : False,
            "format" : "json",
            "options" : {
                "temperature" : 0.1,
                "num_predict" : 500
            }
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=300.0)
            response.raise_for_status()
            result = response.json()
            
            raw_llm_text = result.get("response", "{}").strip()
            print(f"RAW LLM OUTPUT: {raw_llm_text}")

            try:
                parsed_json = json.loads(raw_llm_text)

                patch_data = parsed_json.get("suggested_patch", "Patch generation failed.")
                if isinstance(patch_data, (dict, list)):
                    patch_data = json.dumps(patch_data, indent=2)

                commit_data = parsed_json.get("referenced_commit", "None")
                if not isinstance(commit_data, (dict, list)):
                    commit_data = str(commit_data)    

                return {
                    "reasoning": parsed_json.get("reasoning", "No reasoning generated."),
                    "root_cause_analysis": parsed_json.get("root_cause_analysis", "Analysis failed."),
                    "suggested_patch": patch_data,
                    "referenced_commit": commit_data
                }
            except json.JSONDecodeError:
                return {"root_cause_analysis": f"JSON Error: {raw_llm_text}", "suggested_patch": "N/A", "referenced_commit": "None"}

            
        except requests.exceptions.Timeout:
            return {"root_cause_analysis": "Timeout Error", "suggested_patch": "Manual SRE intervention required.", "referenced_commit": "None"}
        except Exception as e:
            return {"root_cause_analysis": f"Pipeline Error: {str(e)}", "suggested_patch": "N/A", "referenced_commit": "None"}

llm_engine = AegisLLMService()        