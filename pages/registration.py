import streamlit as st
import datetime
# main.py mathi client connection import karo
from main import client

st.title("🏗️ Contractor Registration")

# Home par pacha java mate button
if st.button("← Back to Home"):
    st.switch_page("main.py")

st.divider()

# Form logic
with st.form("reg_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        con_name = st.text_input("Contractor Name*")
        agency = st.text_input("Agency Name*")
    
    with col2:
        mobile = st.text_input("Mobile Number")
        work_type = st.selectbox("Work Category", ["RCC", "Masonry", "Plaster", "Plumbing", "Electrical"])
        
    submitted = st.form_submit_button("Register Now")
    
    if submitted:
        if con_name and agency:
            if client:
                try:
                    # Google Sheet 'DWCS TWT' ma 'Contractors' tab hovvu joie
                    sheet = client.open("DWCS TWT").worksheet("Contractors")
                    
                    today = datetime.datetime.now().strftime("%d-%m-%Y")
                    data = [today, con_name, agency, mobile, work_type]
                    
                    sheet.append_row(data)
                    st.success(f"✅ {con_name} Registered Successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Sheet Error: {e}")
            else:
                st.error("Database connection malyu nathi!")
        else:
            st.warning("Please fill Name and Agency details.")

# Optional: Registered data display karva mate
if st.checkbox("Show Registered List"):
    try:
        sheet = client.open("DWCS TWT").worksheet("Contractors")
        st.dataframe(sheet.get_all_records())
    except:
        st.info("No data available yet.")