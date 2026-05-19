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

def fetch_telemetry():
   
   try:
      res = requests.get(f"{API_BASE_URL}/telemetry", timeout=2)
      if res.status_code == 200:
            return res.json()
   except requests.exceptions.ConnectionError:
      pass

   return {"logs": [], "active_incident": None}

live_data = fetch_telemetry()  

feed_col, ai_col = st.columns([1.5, 1])

with feed_col:
    st.subheader("Recent Telemetry Feed")
    if st.session_state.log_history:

        df = pd.DataFrame(st.session_state.log_history)

        def color_anomalies(val):
            color = '#ff4b4b' if 'YES' in str(val) else ''
            return f'color: {color}'
        
        st.dataframe(df.style.map(color_anomalies, subset=['Is Anomaly']), use_container_width=True, hide_index=True)

    else:
        st.info("Awaiting telemetry data... Click a button above to generate traffic.")

with ai_col:
    st.subheader("Aegis AI Diagnostician")

    incident = st.session_state.activate_incident

    if incident:

        st.error("### CRITICAL ANOMALY DETECTED")

        commit_hash = incident.get("referenced_commit")
        if commit_hash == "None"or not commit_hash:
           st.warning("**AI Confidence Low:** Could not isolate culprit commit. Manual SRE Audit Required.")
        else:
           st.success(f"**Culprit Isolated:** Commit `{commit_hash}`")

        tab1, tab2, tab3 = st.tabs(["Root Cause", "Suggested Patch", "AI Scratchpad"])

        with tab1:
          st.write(incident.get("root_cause_analysis", "No RCA provided."))
        with tab2:
          st.code(incident.get("suggested_patch", "No patch provided."), language="markdown")
        with tab3:
          st.caption("The 1B Model's internal reasoning chain:")
          st.text(incident.get("reasoning_scrap", "No reasoning data."))

    else:
       st.success("System stable. No active incidents.")       
                    