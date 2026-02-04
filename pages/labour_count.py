import streamlit as st
from connection import get_gspread_client
import datetime

# page setup for Mobile Look
st.set_page_config(page_title="Labour Counting", layout="centered")


# css For styling of Page
st.markdown("""
    <style>
    .stApp { background-color: #E0F7FA; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        border: none !important;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👷 Labour Counting Page")

col1, col2 = st.columns(2)
with col1:
    count_date = st.date_input("Select Date", datetime.date.today,format="YYYY-MM-DD")
with col2:
    shift = st.selectbox("Select Shift", ["Day", "Night"], horizontal=True)
    
#2. Contractor Data Fatch 
@st.cache_data
def get_contractor_data():
    try:
        client = get_gspread_client()
        sheet = client.open("DWCS TWT").worksheet("Contractors")
        records = sheet.get_all_records()
        return records
    except Exception as e:
        st.error(f"Error fetching contractor data: {e}")
        return [] 
all_records = get_contractor_data()

#2 Category Wise list
categories = sorted(list(set(r["Contractor Category"] for r in all_records if r["Contractor Category"]))) 
