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
            Skill = st.checkbox("Skill")
        with s_col2:
            Skill = st.number_input("Skill", min_value=0.0, format="%.2f",placeholder="0", disabled= not Skill)
        
        # Unskill Sub line
        u_col1, u_col2 = st.columns([1, 1])
        with u_col1:
            Unskill = st.checkbox("Unskill")
        with u_col2:
            Unskill = st.number_input("Unskill", min_value=0.0, format="%.2f",placeholder="0", disabled= not Unskill)
        
        
    with col2:
        category = st.text_input("Category")
        
    submitted = st.form_submit_button("Register Now")
    
    if submitted:
        if con_name and category:
            if client:
                try:
                    # 'Contractors' tab hovvu joie
                    sheet = client.open("DWCS TWT").worksheet("Contractors")
                    data = [datetime.datetime.now().strftime("%d-%m-%Y"), con_name, category, Skill, Unskill]
                    sheet.append_row(data)
                    st.success(f"✅ {con_name} Registered!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Sheet Error: {e}")
            else:
                st.error("Database connection failed!")
        else:
            st.warning("Please fill required fields.")