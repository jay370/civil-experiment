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

with st.container(border=True):
    # પહેલું સિલેક્શન: કેટેગરી
    selected_cat = st.selectbox("Select Contractor Category", options=categories, index=None, placeholder="Choose Category...")

    # બીજું સિલેક્શન: કેટેગરી મુજબના કોન્ટ્રાક્ટર
    filtered_contractors = []
    if selected_cat:
        filtered_contractors = [r['Contractor Site Name'] for r in all_records if r.get('Contractor Category') == selected_cat]
    
    selected_con = st.selectbox("Select Contractor", options=filtered_contractors, index=None, placeholder="Choose Contractor...", disabled=not selected_cat)

    # ૩. ડેટા એન્ટ્રી સેક્શન
    if selected_con:
        st.divider()
        col_name, col_input = st.columns([2, 1])
        
        with col_name:
            st.write(f"Enter Attendance for **{selected_con}**")
            
        with col_input:
            # ટેક્સ્ટ ઇનપુટ જેથી '8+6' લખી શકાય
            raw_val = st.text_input("Count", key=f"cnt_{selected_con}", placeholder="8+6", label_visibility="collapsed")
            
            # ગણતરી લોજિક
            try:
                # જો ખાલી હોય તો 0, નહીંતર '+' થી તોડીને સરવાળો
                calculated_val = sum(int(x.strip()) for x in raw_val.split('+')) if raw_val else 0
            except:
                st.error("Please enter numbers like 8+6")
                calculated_val = 0
        
        # ડિસ્પ્લે ટોટલ
        if calculated_val > 0:
            st.info(f"Total Labour for this entry: **{calculated_val}**")
            
        # ડેટાને લિસ્ટમાં ઉમેરવો (સેવ કરવા માટે)
        all_data = [{"contractor": selected_con, "category": selected_cat, "raw": raw_val, "total": calculated_val}]
    
    