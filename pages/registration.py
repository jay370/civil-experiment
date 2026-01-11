import streamlit as st
import datetime
from connection import get_gspread_client

# પેજ ટાઈટલ
st.title("🏗️ Contractor Registration")

# હોમ પેજ પર પાછા જવા માટે
if st.button("← Back to Home"):
    st.switch_page("main.py")

st.divider()

# ડેટાબેઝ કનેક્શન
client = get_gspread_client()

# ફોર્મની જગ્યાએ સાદું લેઆઉટ (Interactive રાખવા માટે)
col1, col2 = st.columns(2)

with col1:
    con_name = st.text_input("Contractor Name*", placeholder="Enter Name")
    
    st.write("---") # નાની લાઇન
    
    # Skill વિભાગ
    s_col1, s_col2 = st.columns([0.75, 0.75])
    with s_col1:
        # Session state નો ઉપયોગ કરીને તાત્કાલિક અપડેટ થશે
        skill_selected = st.checkbox("Skill", key="skill_check")
    with s_col2:
        skill_rate = st.text_input(
            "Skill Rate (Rs.)", 
            placeholder="0", 
            disabled=not st.session_state.skill_check,
            key="s_rate_val"
        )
            
    # Unskill વિભાગ
    u_col1, u_col2 = st.columns([0.75, 0.75])
    with u_col1:
        unskill_selected = st.checkbox("Unskill", key="unskill_check")
    with u_col2:
        unskill_rate = st.text_input(
            "Unskill Rate (Rs.)", 
            placeholder="0", 
            disabled=not st.session_state.unskill_check,
            key="u_rate_val"
        )

with col2:
    category = st.text_input("Work Category", placeholder="Shuttering,Steel,etc.")
    location = st.text_input("Location/City")
    contact = st.text_input("Contact Number")

st.divider()

# આ કોડ "Register Now" બટન દબાવ્યા પછીના ભાગમાં મૂકવો

if st.button("🚀 Register Now", use_container_width=True):
    if con_name and category:
        if client:
            try:
                sheet = client.open("DWCS TWT").worksheet("Contractors")
                
                # 1. VBA ની જેમ પહેલા ટેબલનું હેડર શોધો (ગમે ત્યાં હોય)
                try:
                    header_cell = sheet.find("NAME OF CONTRACTOR")
                    header_row = header_cell.row
                    header_col = header_cell.col
                except:
                    # જો હેડર ન મળે તો ડિફોલ્ટ પેલી રો ગણવી
                    header_row = 1
                    header_col = 1

                # 2. ડેટા તૈયાર કરો (તમારી 8 કોલમ મુજબ)
                l_type1 = "Skill" if st.session_state.skill_check else ""
                l_type2 = "Unskill" if st.session_state.unskill_check else ""
                s_rate = skill_rate if st.session_state.skill_check else "0"
                u_rate = unskill_rate if st.session_state.unskill_check else "0"

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

                # 3. VBA સ્ટાઇલ ઇન્સર્ટ (insert_row)
                # આ ફંક્શન હેડરની નીચે નવી રો બનાવશે અને જૂનો ડેટા નીચે ધકેલશે
                # આનાથી ટેબલની ફોર્મેટિંગ અને ફોર્મ્યુલા જળવાઈ રહેશે
                sheet.insert_row(
                    data_to_save, 
                    index=header_row + 1, # હેડરની તરત નીચેની લાઈન
                    value_input_option='USER_ENTERED'
                )
                
                st.success(f"✅ {con_name} નો ડેટા ટેબલમાં 'Insert' થઈ ગયો છે!")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error: {e}")