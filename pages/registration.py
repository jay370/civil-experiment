import streamlit as st
import datetime
from connection import get_gspread_client

st.title("🏗️ Contractor Registration")

if st.button("← Back to Home"):
    st.switch_page("main.py")

st.divider()

# ડેટાબેઝ કનેક્શન
client = get_gspread_client()

# --- સેવ કરવાનું ફંક્શન (બટન ક્લિક પર ચાલશે) ---
def save_data():
    if st.session_state.con_name_val and st.session_state.category_val:
        try:
            sheet = client.open("DWCS TWT").worksheet("Contractors")
            
            # VBA સ્ટાઇલ: હેડર શોધો
            try:
                header_cell = sheet.find("NAME OF CONTRACTOR")
                header_row = header_cell.row
            except:
                header_row = 1

            # ડેટા તૈયાર કરો
            l_type1 = "Skill" if st.session_state.skill_check_val else ""
            l_type2 = "Unskill" if st.session_state.unskill_check_val else ""
            s_rate = st.session_state.s_rate_val if st.session_state.skill_check_val else "0"
            u_rate = st.session_state.u_rate_val if st.session_state.unskill_check_val else "0"

            data_to_save = [
                datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                str(st.session_state.con_name_val).upper(),
                str(st.session_state.category_val).upper(),
                str(l_type1),
                str(l_type2),
                str(s_rate),
                str(u_rate),
                str(st.session_state.contact_val)
            ]

            # ડેટા ઇન્સર્ટ કરો
            sheet.insert_row(data_to_save, index=header_row + 1, value_input_option='USER_ENTERED')
            
            # બધી વેલ્યુ ક્લિયર કરો (અહીં ક્લિયર કરવાથી એરર નહીં આવે)
            st.session_state.con_name_val = ""
            st.session_state.category_val = ""
            st.session_state.location_val = ""
            st.session_state.contact_val = ""
            st.session_state.s_rate_val = "0"
            st.session_state.u_rate_val = "0"
            st.session_state.skill_check_val = False
            st.session_state.unskill_check_val = False
            
            st.toast("✅ Registration Successful!", icon="🎉")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill Name and Category!")

# --- UI (Layout) ---
col1, col2 = st.columns(2)

with col1:
    st.text_input("Contractor Name*", placeholder="Enter Name", key="con_name_val")
    st.write("---")
    
    s_col1, s_col2 = st.columns([0.75, 0.75])
    with s_col1:
        st.checkbox("Skill", key="skill_check_val")
    with s_col2:
        st.text_input("Skill Rate (Rs.)", placeholder="0", 
                      disabled=not st.session_state.skill_check_val, key="s_rate_val")
            
    u_col1, u_col2 = st.columns([0.75, 0.75])
    with u_col1:
        st.checkbox("Unskill", key="unskill_check_val")
    with u_col2:
        st.text_input("Unskill Rate (Rs.)", placeholder="0", 
                      disabled=not st.session_state.unskill_check_val, key="u_rate_val")

with col2:
    st.text_input("Work Category", key="category_val")
    st.text_input("Location/City", key="location_val")
    st.text_input("Contact Number", key="contact_val")

st.divider()

# 'on_click' નો ઉપયોગ કરવાથી એરર ગાયબ થઈ જશે
st.button("🚀 Register Now", on_click=save_data, use_container_width=True)