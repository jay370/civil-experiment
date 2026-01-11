import streamlit as st
import datetime
from connection import get_gspread_client # connection.py mathi lyo

# Ahiya st.set_page_config() na nakhvu

st.title("🏗️ Contractor Registration")

# Back to Home button
if st.button("← Back to Home"):
    st.switch_page("main.py")

st.divider()

# Connection load karo
client = get_gspread_client()

with st.form("reg_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        con_name = st.text_input("Contractor Name*")

        # Skill Sub line
        s_col1, s_col2 = st.columns([1,1])
        with s_col1:
            skill_selected = st.checkbox("Skill")
        with s_col2:
            skill_rate = st.text_input("Skill", min_value=0.0,placeholder="0",disabled=not skill_selected)
        
        # Unskill Sub line
        u_col1, u_col2 = st.columns([1, 1])
        with u_col1:
           unskill_selected = st.checkbox("Unskill")
        with u_col2:
            unskill_rate = st.text_input("Unskill", min_value=0.0,placeholder="0",disabled=not unskill_selected)

    with col2:
        category = st.text_input("Category")
        
    submitted = st.form_submit_button("Register Now")
    
    if submitted:
        if con_name and category:
            if client:
                try:
                    # 'Contractors' tab hovvu joie
                    sheet = client.open("DWCS TWT").worksheet("Contractors")
                    data = [datetime.datetime.now().strftime("%d-%m-%Y"), con_name, category, skill_rate, unskill_rate]
                    sheet.append_row(data)
                    st.success(f"✅ {con_name} Registered!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Sheet Error: {e}")
            else:
                st.error("Database connection failed!")
        else:
            st.warning("Please fill required fields.")