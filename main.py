import streamlit as st
import registration  # registration.py file ne import karo
import gspread
from google.oauth2.service_account import Credentials
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Civil Site App", layout="centered")

# --- 2. HIDE STREAMLIT ELEMENTS ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stGithubIcon {display: none;}
            .stDeployButton {display: none;} 
            [data-testid="stToolbar"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. SESSION STATE (Page Control mate) ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# --- 4. GOOGLE SHEETS CONNECTION ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def get_gspread_client():
    try:
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info).with_scopes(SCOPES)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Secrets Error: {e}")
        return None

client = get_gspread_client()

# --- 5. NAVIGATION LOGIC ---

# --- PAGE 1: HOME ---
if st.session_state.current_page == 'Home':
    st.title("🏗️ Civil Site Experiment App")
    
    st.write("Welcome to the main dashboard.")
    
    # Button thi Registration page par java mate
    if st.button("Contractor Registration Page par jao"):
        st.session_state.current_page = 'Reg'
        st.rerun() # Page refresh kari ne navi screen batavshe

    # Database connectivity status check
    if client:
        st.sidebar.success("Connected to Database ✅")
    else:
        st.sidebar.error("Database connection failed ❌")

# --- PAGE 2: REGISTRATION ---
elif st.session_state.current_page == 'Reg':
    # Back button home par pacha java mate
    if st.button("← Back to Dashboard"):
        st.session_state.current_page = 'Home'
        st.rerun()
    
    st.divider()
    
    # Registration module mathi form load thase
    # Khatri karjo ke registration.py ma 'show_registration()' function che
    try:
        registration.show_registration()
    except AttributeError:
        st.error("Error: 'registration.py' ma 'show_registration()' function nathi malyu!")