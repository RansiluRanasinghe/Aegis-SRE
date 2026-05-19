import requests
import time
import random

API_URL = "http://localhost:8000/api/v1/analyze"

print("Aegis Background Agent Initialized.")
print("Simulating live server traffic. Press Ctrl+C to stop.\n")

counter = 0

while True:
    counter += 1

    if counter % 20 == 0:
        print("INJECTING ANOMALY: Brute Force Attack!")
        payload = {"bytes": 120.0, "status": 401, "hour": 2, "ip_freq": 850, "is_error": 1}

    elif counter % 35 == 0:
        print("INJECTING ANOMALY: Cache Crash!")
        payload = {"bytes": 0.0, "status": 502, "hour": 14, "ip_freq": 12, "is_error": 1}

    else:
        print("Sending normal web traffic...")
        payload = {
            "bytes": random.randint(500, 5000), 
            "status": 200, 
            "hour": random.randint(8, 18), 
            "ip_freq": random.randint(1, 10), 
            "is_error": 0
        }

    try:
        requests.post(API_URL, json=payload)
    except Exception as e:
        print(f"Error sending data: {e}")

    time.sleep(2)                      