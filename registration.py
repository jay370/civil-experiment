import streamlit as st
import datetime

# Aa mukhya function che jene main.py mathi call karvama avshe
def show_registration():
    st.header("🏗️ New Contractor Registration")
    st.write("Ahiya thi tame nava contractor ne system ma register kari shakosho.")

    # Form banavo jethi 'Submit' dabo tyare j data upload thay
    with st.form("contractor_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            con_name = st.text_input("Contractor Full Name*")
            agency_name = st.text_input("Agency / Company Name*")
        
        with col2:
            contact_no = st.text_input("Mobile Number")
            work_type = st.selectbox("Work Category", ["RCC", "Masonry", "Plaster", "Plumbing", "Electrical", "Flooring"])
        
        # Form Submit Button
        reg_submitted = st.form_submit_button("Register Contractor")
        
        if reg_submitted:
            # Check karo ke mukhya details bhari che ke nahi
            if con_name and agency_name:
                try:
                    # main.py ma banavela 'client' no upyog karvo
                    # Pan ahiya aapne simple connectivity check kariye
                    from main import client
                    
                    if client:
                        # Google Sheet 'DWCS TWT' ma 'Contractors' naam nu tab hovvu joie
                        # Jo tab na hoy to sheet.gsheet_client.open mathi open karvu pade
                        sheet = client.open("DWCS TWT").worksheet("Contractors")
                        
                        # Data prepare karo
                        today = datetime.datetime.now().strftime("%d-%m-%Y")
                        new_row = [today, con_name, agency_name, contact_no, work_type]
                        
                        # Sheet ma line add karo
                        sheet.append_row(new_row)
                        
                        st.success(f"✅ {con_name} ({agency_name}) successfully register thai gaya che!")
                        st.balloons()
                    else:
                        st.error("Database connection malyu nathi. Please check main.py.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("💡 Tip: Google Sheet ma 'Contractors' naam nu navu 'Tab' (Worksheet) banavo.")
            else:
                st.warning("⚠️ Name ane Agency Name nakhvu jaroori che!")

# Aa function niche data display karva mate che (Optional)
    if st.checkbox("Show Registered Contractors List"):
        try:
            from main import client
            sheet = client.open("DWCS TWT").worksheet("Contractors")
            data = sheet.get_all_records()
            if data:
                st.dataframe(data)
            else:
                st.info("Haju koi contractor register nathi thaya.")
        except:
            pass