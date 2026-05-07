import streamlit as st
import requests
import time
import pandas as pd
import random

st.set_page_config(
    page_title="Aegis Commander",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://localhost:8000/api/v1"

with st.sidebar:
    st.title("Aegis Commander")
    st.markdown("Autonomous SRE Diagnostics")
    st.markdown("---")

    st.subheader("System Status")

    try:
        health_res = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if health_res.status_code == 200:
            data = health_res.json()
            st.success("Backend: Online")
            st.caption(f"**ML Engine:** {data.get('engine')}")
            st.caption(f"**AI Engine:** {data.get('llm_engine')}")
        else:
            st.warning("Backend: Degraded")

    except requests.exceptions.ConnectionError:
        st.error("Backend: Offline")
        st.caption("Ensure Uvicorn is running on port 8000.")

st.title("Live Telemetry & Diagnostics")
st.markdown("Monitoring incoming API traffic for statistical anomalies...")

if "log_history" not in st.session_state:
    st.session_state.log_history = []
if "activate_incident" not in st.session_state:
    st.session_state.activate_incident = None

st.subheader("Traffic Control Panel")
st.caption("Simulate real-time log ingestion.")

col1, col2, col3, col4 = st.columns(4)

def send_traffic(payload, label):

    with st.spinner(f"Ingesting {label}..."):

        try:
            res = requests.post(f"{API_BASE_URL}/analyze", json=payload, timeout=60)
            if res.status_code == 200:
                data = res.json()

                new_log = {
                    "Timestamp": time.strftime("%H:%M:%S"),
                    "Type": label,
                    "Status": payload["status"],
                    "Bytes": payload["bytes"],
                    "Freq": payload["ip_freq"],
                    "ML Score": round(data["confidence_score"], 3),
                    "Is Anomaly": "YES" if data["is_anomaly"] else "NO"
                }

                st.session_state.log_history.insert(0, new_log)
                st.session_state.log_history = st.session_state.log_history[:10]

                if data["is_anomaly"]:
                    st.session_state.activate_incident = data
                else:
                    st.session_state.activate_incident = None

        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to backend API.")

with col1:
    if st.button("Noraml Traffic", use_container_width=True):
        send_traffic({"bytes": random.randint(500, 5000), "status": 200, "hour": 12, "ip_freq": random.randint(1, 10), "is_error": 0}, "Normal")

with col2:
    if st.button("Brute Force", use_container_width=True):
        send_traffic({"bytes": 120.0, "status": 401, "hour": 2, "ip_freq": 850, "is_error": 1}, "Brute Force")

with col3:
    if st.button("Exfiltration", use_container_width=True):
        send_traffic({"bytes": 5000000000.0, "status": 200, "hour": 14, "ip_freq": 2, "is_error": 0}, "Exfiltration")

with col4:
    if st.button("Cache Crash", use_container_width=True):
        send_traffic({"bytes": 0.0, "status": 502, "hour": 14, "ip_freq": 12, "is_error": 1}, "Crash Loop") 

st.markdown("---")               