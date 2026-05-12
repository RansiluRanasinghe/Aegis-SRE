import requests
import json

API_URL = "http://localhost:8000/api/v1/analyze"

print("🛡️ Initiating Aegis-SRE Production Certification Test...\n")

# THE SCENARIO: 
# Peak business hours (14:00). 
# Normal user traffic (ip_freq: 12 - NOT a brute force).
# The backend suddenly drops the connection (502 Bad Gateway, 0 bytes).
payload = {
    "bytes": 0.0,
    "status": 502, 
    "hour": 14,    
    "ip_freq": 12, 
    "is_error": 1
}

print(f"[Scenario: The Silent Cache Explosion]")
print(f"Payload: {json.dumps(payload)}\n")

try:
    response = requests.post(API_URL, json=payload, timeout=300.0)
    result = response.json()

    print(f"ML Confidence Score: {result['confidence_score']:.3f}")
    print(f"Culprit Commit: [{result.get('referenced_commit', 'None')}]")
    print(f"Root Cause Analysis:\n{result.get('root_cause_analysis', 'Failed to generate.')}\n")
    print(f"Suggested Patch:\n{result.get('suggested_patch', 'Failed to generate.')}\n")

except Exception as e:
    print(f"Pipeline Error: {str(e)}")