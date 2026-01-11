
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Civil Site App", layout="centered")

# --- 2. HIDE STREAMLIT ELEMENTS (Optional - Clean Look mate) ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display: none;} 
            [data-testid="stToolbar"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. GOOGLE SHEETS CONNECTION SETUP ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def get_gspread_client():
    try:
        # Streamlit Cloud na Secrets mathi data lese
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info).with_scopes(SCOPES)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Secrets Configuration Error: {e}")
        return None

# Connection object banavo jene bija pages mathi import kari shakay
client = get_gspread_client()

# --- 4. HOME UI ---
st.title("🏗️ Civil Site Management System")
st.write("Welcome to the Home Page. Please use the sidebar or the button below to navigate.")

if client:
    st.sidebar.success("Database Connected ✅")
    
    # Navigation Button
    if st.button("Go to Contractor Registration"):
        # Pages folder vali rit mate sacho path
        st.switch_page("pages/registration.py")
else:
    st.sidebar.error("Database Connection Failed ❌")