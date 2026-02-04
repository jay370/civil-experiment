import streamlit as st
from connection import get_gspread_client
import datetime

# --- Page Setup ---
st.set_page_config(page_title="Labour Counting", layout="centered")

# --- CSS for Mobile Look ---
st.markdown("""
    <style>
    .stApp { background-color: #007AFF; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #007AFF;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("☀️ Daily Labour Counting")

# ૧. તારીખ અને શિફ્ટ સિલેક્શન
col1, col2 = st.columns(2)
with col1:
    count_date = st.date_input("Select Date", datetime.date.today())
with col2:
    shift = st.radio("Shift", ["Day", "Night"], horizontal=True)

# ૨. કોન્ટ્રાક્ટર ડેટા ફેચિંગ (આપણે અગાઉ બનાવેલી શીટમાંથી)
@st.cache_data
def get_contractor_list():
    try:
        client = get_gspread_client()
        sheet = client.open("DWCS TWT").worksheet("Contractors")
        records = sheet.get_all_records()
        # ફક્ત સાઇટના નામનું લિસ્ટ
        return [r['Contractor Site Name'] for r in records]
    except:
        return ["Amarsing NAKA", "Somsing"] # બેકઅપ લિસ્ટ

contractors = get_contractor_list()

# ૩. ડાયનેમિક કાઉન્ટિંગ ફોર્મ
st.subheader(f"Enter Counts for {shift} Shift")

# આપણે આમાં યુઝર પાસે '8+6' જેવું ઇનપુટ લેવા માંગીએ છીએ
all_data = []
total_labour = 0

with st.container(border=True):
    for con in contractors:
        col_name, col_input = st.columns([2, 1])
        with col_name:
            st.write(f"**{con}**")
        with col_input:
            # ટેક્સ્ટ ઇનપુટ જેથી '8+6' લખી શકાય
            raw_val = st.text_input("Count", key=f"cnt_{con}", placeholder="0+0", label_visibility="collapsed")
            
            # ગણતરી લોજિક
            try:
                # જો ખાલી હોય તો 0, નહીંતર '+' થી તોડીને સરવાળો
                calculated_val = sum(int(x.strip()) for x in raw_val.split('+')) if raw_val else 0
            except:
                calculated_val = 0
            
            all_data.append({"contractor": con, "raw": raw_val, "total": calculated_val})
            total_labour += calculated_val

st.metric("Total Labour on Site", total_labour)

# ૪. સેવ બટન
if st.button("Save Attendance", use_container_width=True):
    try:
        client = get_gspread_client()
        # નવી શીટ 'Labour_Attendance' હોવી જોઈએ
        sheet = client.open("DWCS TWT").worksheet("Labour_Attendance")
        
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        
        rows_to_add = []
        for entry in all_data:
            if entry['total'] > 0: # ફક્ત જેમાં એન્ટ્રી હોય તે જ સેવ કરો
                rows_to_add.append([
                    str(count_date),
                    shift,
                    entry['contractor'],
                    entry['raw'],
                    entry['total'],
                    timestamp
                ])
        
        if rows_to_add:
            sheet.append_rows(rows_to_add)
            st.success(f"✅ {len(rows_to_add)} Contractors' data saved!")
            st.balloons()
        else:
            st.warning("No data to save!")
            
    except Exception as e:
        st.error(f"Error: {e}. Make sure 'Labour_Attendance' sheet exists.")