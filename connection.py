import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Scopes define karo
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def get_gspread_client():
    try:
        # Streamlit Secrets mathi data lese
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info).with_scopes(SCOPES)
        return gspread.authorize(creds)
    except Exception as e:
        return None