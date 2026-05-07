import streamlit as st
import requests

st.set_page_config(
    page_title="Aegis Commander",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://localhost:8000/api/v1"