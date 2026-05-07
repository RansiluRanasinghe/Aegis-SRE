import streamlit as st
import requests

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