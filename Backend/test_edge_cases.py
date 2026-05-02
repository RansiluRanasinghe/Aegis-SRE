import requests
import time
import json

API_URL = "http://localhost:8000/api/v1/analyze"

edge_cases = {
    "1. The Brute Force Attack (Scanner Bot)": {
        "bytes": 120.0,
        "status": 401,
        "hour": 2,        
        "ip_freq": 850,   
        "is_error": 1
    },
    "2. The Data Exfiltration (Silent Theft)": {
        "bytes": 5000000000.0,
        "status": 200,
        "hour": 14,
        "ip_freq": 2,
        "is_error": 0
    },
    "3. The Application Crash Loop": {
        "bytes": 0.0,
        "status": 503,
        "hour": 9,
        "ip_freq": 15,
        "is_error": 1
    }
}

print("Initiating Aegis-SRE Edge Case Chaos Testing...\n")

for attack_name, payload in edge_cases.items():
    print(f"[{attack_name}]")
    print(f"Payload: {json.dumps(payload)}")

    try:

        response = requests.post(API_URL, json=payload, timeout=60.0)
        result = response.json()

        print(f"ML Confidence Score: {result['confidence_score']:.3f}")
        rca = result.get("root_cause_analysis", "No RCA provided.")
        patch = result.get("suggested_patch", "No patch provided.")
        commit = result.get('referenced_commit', 'None')

        print(f"Culprit Commit: [{commit}]")
        print(f"Root Cause Analysis:\n{rca}\n")
        print(f"Suggested Patch:\n{patch}\n")
        print("....................................\n")

    except Exception as e:
        print(f"Error during testing: {str(e)}\n")

    time.sleep(2)  # Pause between tests to simulate real-world conditions        