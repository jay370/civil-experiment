import streamlit as st
import datetime

def show_registration(sheet):
    st.subheader("🏗️ New Contractor Registration")
    
    with st.form("reg_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            con_name = st.text_input("Contractor Name")
            agency = st.text_input("Agency/Company Name")
        
        with col2:
            mobile = st.text_input("Mobile Number")
            work_type = st.selectbox("Work Type", ["RCC", "Masonry", "Plaster", "Flooring", "Painting"])
            
        submitted = st.form_submit_button("Register Now")
        
        if submitted:
            if con_name and agency:
                # Google Sheet ma data nakhvo
                # Order: Date, Name, Agency, Mobile, WorkType
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                data = [today, con_name, agency, mobile, work_type]
                
                try:
                    # 'Contractors' naam na worksheet ma data jashe
                    con_sheet = sheet.gsheet_client.open("DWCS TWT").worksheet("Contractors")
                    con_sheet.append_row(data)
                    st.success(f"✅ {con_name} registered successfully!")
                except Exception as e:
                    st.error(f"Error: {e}. Check if 'Contractors' tab exists in Sheet.")
            else:
                st.warning("Please fill Name and Agency details.")