import streamlit as st
import datetime
from connection import get_gspread_client

# પેજ સેટઅપ
st.set_page_config(page_title="Contractor Registration", layout="wide")

st.title("🏗️ Contractor Registration")

# હોમ પેજ પર પાછા જવા માટે
if st.button("← Back to Home"):
    st.switch_page("main.py")

st.divider()

# ડેટાબેઝ કનેક્શન
client = get_gspread_client()

# ઇનપુટ લેઆઉટ
col1, col2 = st.columns(2)

with col1:
    # કી (key) હંમેશા સ્મોલ 'k' માં રાખવી
    con_name = st.text_input("Contractor Name*", placeholder="Enter Name", key="con_name_val")
    
    st.write("---")
    
    # Skill વિભાગ
    s_col1, s_col2 = st.columns([0.75, 0.75])
    with s_col1:
        skill_selected = st.checkbox("Skill", key="skill_check_val")
    with s_col2:
        skill_rate = st.text_input(
            "Skill Rate (Rs.)", 
            placeholder="0", 
            disabled=not st.session_state.get('skill_check_val', False),
            key="s_rate_val"
        )
            
    # Unskill વિભાગ
    u_col1, u_col2 = st.columns([0.75, 0.75])
    with u_col1:
        unskill_selected = st.checkbox("Unskill", key="unskill_check_val")
    with u_col2:
        unskill_rate = st.text_input(
            "Unskill Rate (Rs.)", 
            placeholder="0", 
            disabled=not st.session_state.get('unskill_check_val', False),
            key="u_rate_val"
        )

with col2:
    category = st.text_input("Work Category", placeholder="Shuttering, Steel, etc.", key="category_val")
    location = st.text_input("Location/City", placeholder="Enter Location", key="location_val")
    contact = st.text_input("Contact Number", placeholder="Enter Contact No.", key="contact_val")

st.divider()

# સેવ કરવાનું લોજિક
if st.button("🚀 Register Now", use_container_width=True):
    if con_name and category:
        if client:
            try:
                # ગૂગલ શીટ ઓપન કરો
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
                    str(con_name).upper(),
                    str(category).upper(),
                    str(l_type1),
                    str(l_type2),
                    str(s_rate),
                    str(u_rate),
                    str(contact)
                ]

                # ટેબલમાં ડેટા ઇન્સર્ટ કરો (VBA સ્ટાઇલ)
                sheet.insert_row(data_to_save, index=header_row + 1, value_input_option='USER_ENTERED')

                # સફળતાનો મેસેજ
                st.success(f"✅ {con_name} Registered Successfully!")
                st.balloons()

                # --- ડેટા ક્લિયર કરવાનું લોજિક ---
                # એરર ટાળવા માટે સીધું જ સ્ટેટ ક્લિયર કરો
                st.session_state.con_name_val = ""
                st.session_state.category_val = ""
                st.session_state.location_val = ""
                st.session_state.contact_val = ""
                st.session_state.s_rate_val = "0"
                st.session_state.u_rate_val = "0"
                st.session_state.skill_check_val = False
                st.session_state.unskill_check_val = False
                
                # પેજને રીફ્રેશ કરો જેથી નવું કોરું ફોર્મ દેખાય
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Google Sheets Connection Failed!")
    else:
        st.warning("Please fill required fields (Name and Category).")