import pandas as pd
import requests
import time
import sys

API_URL = "http://localhost:8000/api/v1/analyze"
DATA_PATH = "data/sample_logs.csv"