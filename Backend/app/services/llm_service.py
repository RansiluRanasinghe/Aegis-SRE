import requests
import json
import os
from pathlib import Path
from app.core.config import settings
from app.core.rule_engine import evaluate_anomaly

class AegisLLMService:

    def __init__(self):
        self.api_url = settings.OLLAMA_API_URL
        self.model = settings.LLM_MODEL

        print(f"Aegis-SRE: GenAI Engine initialized. Target: {self.api_url} ({self.model})")

    def _get_repo_context(self, system_diagnosis: str) -> str:

        base_dir = Path(__file__).resolve().parent.parent
        context_path = base_dir / "context" / "repo_context.json"  

        try:
            with open(context_path, "r") as f:
                data = json.load(f)

            context_str =  f"Architecture Notes: {data['architecture_notes']}\n\nRecent Commits:\n"

            keywords = []
            if "auth" in system_diagnosis.lower() or "rate limit" in system_diagnosis.lower():
                keywords = ["auth", "login", "rate limit", "security"]
            elif "payload" in system_diagnosis.lower() or "data" in system_diagnosis.lower():
                keywords = ["payload", "data", "size", "download"]
            elif "memory" in system_diagnosis.lower() or "backend" in system_diagnosis.lower():
                keywords = ["cache", "memory", "refactor", "dict"]

            filtered_commits = []
            for commit in data["recent_commits"]:
                if not keywords or any(kw in commit["message"].lower() for kw in keywords):
                    filtered_commits.append(commit)

            if not filtered_commits:
                filtered_commits = data["recent_commits"]

            for commit in filtered_commits:
                context_str += f"- [{commit['hash']}] {commit['author']}: {commit['message']}\n"  

            return context_str              

        except FileNotFoundError:
            return "No repository context found."
        except Exception as e:
            return f"Error loading repository context: {str(e)}"

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

        system_context = self._get_repo_context()          

        prompt = f"""You are Aegis-SRE, an autonomous AI Diagnostician. 
Determine the root cause of this anomaly by comparing the system logs to the architectural context and recent Git commits.

[ARCHITECTURAL CONTEXT & RECENT COMMITS]
{system_context}

[RECENT TRAFFIC HISTORY]
{history_str}

[ANOMALY TRIGGER]
Status Code: {status} | Payload Size: {bytes_size} bytes | IP Frequency: {ip_freq}

[RULE ENGINE HINT]
{system_diagnosis}

Based purely on the context above, write a Root Cause Analysis (RCA) explaining what caused the anomaly, and a Suggested Patch to fix it.

You must respond ONLY with a valid JSON object using this exact structure. You MUST generate the "reasoning" key first:
        {{
          "reasoning": "Think step-by-step. 1) What is the symptom? 2) Which specific commit explains this symptom? 3) How do we fix it?",
          "root_cause_analysis": "Your formal explanation goes here.",
          "suggested_patch": "Your code or configuration patch goes here.",
          "referenced_commit": "The exact 7-character commit hash responsible, or 'None'"
        }}
"""
        
        payload = {
            "model" : self.model,
            "prompt" : prompt,
            "stream" : False,
            "format" : "json",
            "options" : {
                "temperature" : 0.1,
                "num_predict" : 200
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
                return {
                    "root_cause_analysis": parsed_json.get("root_cause_analysis", "Analysis failed."),
                    "suggested_patch": parsed_json.get("suggested_patch", "Patch generation failed."),
                    "referenced_commit": parsed_json.get("referenced_commit", "None")
                }
            except json.JSONDecodeError:
                return {"root_cause_analysis": f"JSON Error: {raw_llm_text}", "suggested_patch": "N/A", "referenced_commit": "None"}

            
        except requests.exceptions.Timeout:
            return {"root_cause_analysis": "Timeout Error", "suggested_patch": "Manual SRE intervention required.", "referenced_commit": "None"}
        except Exception as e:
            return {"root_cause_analysis": f"Pipeline Error: {str(e)}", "suggested_patch": "N/A", "referenced_commit": "None"}

llm_engine = AegisLLMService()        