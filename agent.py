import requests
import time
import random

API_URL = "http://localhost:8000/api/v1/analyze"

print("Aegis Background Agent Initialized.")
print("Simulating live server traffic. Press Ctrl+C to stop.\n")

counter = 0

while True:
    counter += 1

    ip_address = f"192.168.1.{random.randint(1, 254)}"

    if counter % 40 == 0:
        print(f"{counter}: INJECTING ANOMALY: Brute Force Attack!")
        payload = {"bytes": 120.0, "status": 401, "hour": 2, "ip_freq": 850, "is_error": 1, "ip_address": "10.0.0.5"}

    elif counter % 75 == 0:
        print(f"{counter}: INJECTING ANOMALY: Cache Crash!")
        payload = {"bytes": 0.0, "status": 502, "hour": 14, "ip_freq": 12, "is_error": 1, "ip_address": ip_address}

    else:
        print(f"{counter}: Sending normal web traffic...")
        payload = {
            "bytes": random.randint(500, 5000), 
            "status": 200, 
            "hour": random.randint(8, 18), 
            "ip_freq": random.randint(1, 10), 
            "is_error": 0,
            "ip_address": ip_address
        }

    try:
        response = requests.post(API_URL, json=payload, timeout=10.0)
        response.raise_for_status()
    except Exception as e:
        print(f"Server busy/unresponsive, retrying in 5s... ({type(e).__name__})")
        time.sleep(5)
        continue

    time.sleep(2)                      