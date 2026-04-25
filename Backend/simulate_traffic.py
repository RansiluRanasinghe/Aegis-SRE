import pandas as pd
import requests
import time
import sys

API_URL = "http://localhost:8000/api/v1/analyze"
DATA_PATH = "data/sample_logs.csv"

def simulate():

    print("Loading Data from, ", DATA_PATH)

    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print("Error: sample_logs.csv not found in the data/ directory.")
        sys.exit(1)

    print("Firing logs at Aegis-SRE API... (Press Ctrl+C to stop)\n")

    for index, row in df.iterrows():

        payload = {
            "bytes": float(row['bytes']),
            "status": int(row['status']),
            "hour": int(row['hour']),
            "ip_freq": int(row['ip_freq']),
            "is_error": int(row['is_error'])
        }

        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()

            if result.get("is_anomaly"):
                print(f"[ANOMALY DETECTED] IP: {row['ip']} | Status: {row['status']} | Bytes: {row['bytes']}")
                print(f"=Score: {result['confidence_score']:.3f} - Waking GenAI Agent...\n")
                time.sleep(1.5)
            else:
               print(f"[NORMAL] Score: {result['confidence_score']:.3f}")

        except requests.exceptions.ConnectionError:
            print("❌ Error: API is offline. Did you start the Uvicorn server?")
            break          