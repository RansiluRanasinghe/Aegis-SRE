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