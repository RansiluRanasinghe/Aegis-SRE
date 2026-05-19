import requests
import time
import random

API_URL = "http://localhost:8000/api/v1/analyze"

print("Aegis Background Agent Initialized.")
print("Simulating live server traffic. Press Ctrl+C to stop.\n")

counter = 0