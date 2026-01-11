import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Civil Site App", layout="centered")

# --- HIDE STREAMLIT ELEMENTS ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stGithubIcon {display: none;}
            /* Aa line Deploy (Paper Crane) icon ne hide karshe */
            .stDeployButton {display: none;} 
            /* Aa line upar ni toolbar ne pura puri kadhi nakhshe */
            [data-testid="stToolbar"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- GOOGLE SHEETS SCOPES ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# --- CONNECTION FUNCTION ---
@st.cache_resource
def get_gspread_client():
    try:
        # Streamlit Secrets mathi data lese
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info).with_scopes(SCOPES)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Secrets Configuration ma bhul che: {e}")
        return None

# --- APP UI ---
st.title("Civil Site Experiment App")

#-- Page Navigation --- 
if st.button("Contractor Registration"):
    st.switch_page("pages/registration.py")
    
client = get_gspread_client()
sheet = None

if client:
    try:
        # Sheet nu naam exact match thavu joie
        sheet = client.open("DWCS TWT").sheet1
        st.sidebar.success("Connected to Database ✅")
    except Exception as e:
        st.sidebar.error("Sheet 'DWCS TWT' nathi mali!")
        st.error(f"Error: {e}")
        st.info("Check karo: 1. Sheet naam 'DWCS TWT' che? 2. Email share karyo che?")

else:
    st.warning("Sheet sathe connection nathi, etle form nahi dekhay.")


