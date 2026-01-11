import streamlit as st
from registration import show_registration # ragistaration module mathi import karo 
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

tab1,tab2 = st.tabs(["Registration","Daily Report"])

with tab1:
    show_registration()

with tab2:
    st.write("Fill the form below to log daily site data.")

client = get_gspread_client()
sheet = None

if client:
    try:
        # Sheet nu naam exact match thavu joie
        sheet = client.open("DWCS TWT").sheet1
        st.sidebar.success("Connected to Google Sheet! ✅")
    except Exception as e:
        st.sidebar.error("Sheet 'DWCS TWT' nathi mali!")
        st.error(f"Error: {e}")
        st.info("Check karo: 1. Sheet naam 'DWCS TWT' che? 2. Email share karyo che?")

# --- ENTRY FORM ---
if sheet:
    with st.form("entry_form", clear_on_submit=True):
        st.subheader("Navi Data Entry")
        
        eng_name = st.selectbox("Engineer Name", ["Rahul", "Suresh", "Amit", "Jay"])
        site_location = st.text_input("Site Location")
        material_bags = st.number_input("Cement Bags", min_value=0, step=1)
        remarks = st.text_area("Remarks (Optional)")
        
        submitted = st.form_submit_button("Submit Data")

        if submitted:
            if site_location == "":
                st.warning("Please enter Site Location!")
            else:
                try:
                    with st.spinner("Saving data..."):
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        data_row = [timestamp, eng_name, site_location, material_bags, remarks]
                        sheet.append_row(data_row)
                        st.success("Data successfully saved! 🚀")
                        st.balloons()
                except Exception as e:
                    st.error(f"Data save nathi thayo: {e}")

    # Data Display
    if st.checkbox("Show Last 5 Entries"):
        try:
            data = sheet.get_all_records()
            if data:
                st.table(data[-5:])
            else:
                st.info("Sheet ma haju koi data nathi.")
        except Exception as e:
            st.error("Data fetch karva ma problem che.")
else:

    st.warning("Sheet sathe connection nathi, etle form nahi dekhay.")


