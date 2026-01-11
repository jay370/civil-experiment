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
        category = st.text_input("Category")
    with col2:
        mobile = st.text_input("Mobile Number")
        work_type = st.selectbox("Work Category", ["RCC", "Masonry", "Plaster", "Plumbing", "Electrical"])
    
    submitted = st.form_submit_button("Register Now")
    
    if submitted:
        if con_name and agency:
            if client:
                try:
                    # 'Contractors' tab hovvu joie
                    sheet = client.open("DWCS TWT").worksheet("Contractors")
                    data = [datetime.datetime.now().strftime("%d-%m-%Y"), con_name, category, mobile, work_type]
                    sheet.append_row(data)
                    st.success(f"✅ {con_name} Registered!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Sheet Error: {e}")
            else:
                st.error("Database connection failed!")
        else:
            st.warning("Please fill required fields.")