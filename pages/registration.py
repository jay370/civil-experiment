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
    s_col1, s_col2 = st.columns([1, 1.5])
    with s_col1:
        # Session state નો ઉપયોગ કરીને તાત્કાલિક અપડેટ થશે
        skill_selected = st.checkbox("Skilled Category", key="skill_check")
    with s_col2:
        skill_rate = st.text_input(
            "Skilled Rate (Rs.)", 
            placeholder="0", 
            disabled=not st.session_state.skill_check,
            key="s_rate_val"
        )
            
    # Unskill વિભાગ
    u_col1, u_col2 = st.columns([1, 1.5])
    with u_col1:
        unskill_selected = st.checkbox("Unskilled Category", key="unskill_check")
    with u_col2:
        unskill_rate = st.text_input(
            "Unskilled Rate (Rs.)", 
            placeholder="0", 
            disabled=not st.session_state.unskill_check,
            key="u_rate_val"
        )

with col2:
    category = st.text_input("Work Category (e.g. Masonry, RCC)", placeholder="RCC, Plaster, etc.")
    location = st.text_input("Location/City")
    contact = st.text_input("Contact Number")

st.divider()

# સેવ કરવાનું બટન
if st.button("🚀 Register Now", use_container_width=True):
    if con_name and category:
        if client:
            try:
                # તમારી ગૂગલ શીટનું નામ "DWCS TWT" અને ટેબ "Contractors"
                sheet = client.open("DWCS TWT").worksheet("Contractors")
                
                # રેટ નક્કી કરવા (જો ટીક ન હોય તો 0)
                final_s_rate = skill_rate if st.session_state.skill_check else "0"
                final_u_rate = unskill_rate if st.session_state.unskill_check else "0"
                
                # ગૂગલ શીટની 7 કોલમ મુજબનો ડેટા
                data_to_save = [
                    datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), # 1. તારીખ અને સમય
                    str(con_name),    # 2. નામ
                    str(category),    # 3. કેટેગરી
                    str(final_s_rate),# 4. સ્કિલ્ડ રેટ
                    str(final_u_rate),# 5. અનસ્કિલ્ડ રેટ
                    str(location),    # 6. લોકેશન
                    str(contact)      # 7. મોબાઈલ નંબર
                ]
                
                sheet.append_row(data_to_save)
                
                st.success(f"સફળતાપૂર્વક નોંધણી થઈ ગઈ: {con_name}")
                st.balloons()
                
            except Exception as e:
                st.error(f"શીટમાં ડેટા સેવ નથી થયો: {e}")
        else:
            st.error("ગૂગલ શીટ સાથે કનેક્શન થઈ શક્યું નથી!")
    else:
        st.warning("કૃપા કરીને નામ અને કેટેગરી જરૂરથી ભરો.")