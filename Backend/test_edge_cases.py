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