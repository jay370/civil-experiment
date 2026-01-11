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
    if con_name and category: # જરૂરી ફિલ્ડ્સ ચેક કરો
        if client:
            try:
                sheet = client.open("DWCS TWT").worksheet("Contractors")
                
                # લોજિક મુજબ ડેટા તૈયાર કરો
                labour_type_1 = "Skill" if st.session_state.skill_check else ""
                labour_type_2 = "Unskill" if st.session_state.unskill_check else ""
                
                # જો રેટ ખાલી હોય તો "0" અથવા યુઝરે લખેલ રેટ
                s_rate = skill_rate if st.session_state.skill_check else "0"
                u_rate = unskill_rate if st.session_state.unskill_check else "0"
                
                # તમારી 8 કોલમ મુજબનો ડેટા (લિસ્ટ)
                data_to_save = [
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), # 1. Date_time
                    str(con_name).upper(),                             # 2. NAME OF CONTRACTOR
                    str(category).upper(),                             # 3. CATEGORY
                    str(labour_type_1),                                # 4. TYPE OF LABOUR 1
                    str(labour_type_2),                                # 5. TYPE OF LABOUR 2
                    str(s_rate),                                       # 6. SKILL RATE
                    str(u_rate),                                       # 7. UNSKILL RATE
                    str(contact)                                       # 8. Mobile Number
                ]
                
                # શીટમાં ડેટા ઉમેરો
                sheet.append_row(data_to_save)
                
                st.success(f"✅ {con_name} નો ડેટા સફળતાપૂર્વક ટેબલમાં સેવ થઈ ગયો છે!")
                st.balloons()
                
            except Exception as e:
                st.error(f"શીટમાં એરર આવી છે: {e}")
        else:
            st.error("ગૂગલ શીટ કનેક્શન મળતું નથી.")
    else:
        st.warning("કૃપા કરીને કોન્ટ્રાક્ટરનું નામ અને કેટેગરી ભરો.")