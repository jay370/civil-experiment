import streamlit as st
import datetime
from connection import get_gspread_client

st.title("🏗️ Contractor Registration")

if st.button("← Back to Home"):
    st.switch_page("main.py")

st.divider()
client = get_gspread_client()

col1, col2 = st.columns(2)

with col1:
    # Key નો 'k' સ્મોલ રાખવો
    con_name = st.text_input("Contractor Name*", placeholder="Enter Name", key="con_name_val")
    
    st.write("---")
    
    s_col1, s_col2 = st.columns([0.75, 0.75])
    with s_col1:
        # ફક્ત એક જ સાચી key રાખો
        skill_selected = st.checkbox("Skill", key="skill_check_val")
    with s_col2:
        skill_rate = st.text_input(
            "Skill Rate (Rs.)", 
            placeholder="0", 
            disabled=not st.session_state.skill_check_val,
            key="s_rate_val"
        )
            
    u_col1, u_col2 = st.columns([0.75, 0.75])
    with u_col1:
        unskill_selected = st.checkbox("Unskill", key="unskill_check_val")
    with u_col2:
        unskill_rate = st.text_input(
            "Unskill Rate (Rs.)", 
            placeholder="0", 
            disabled=not st.session_state.unskill_check_val,
            key="u_rate_val"
        )

with col2:
    category = st.text_input("Work Category", placeholder="Shuttering,Steel,etc.", key="category_val")
    location = st.text_input("Location/City", placeholder="Enter Location", key="location_val")
    contact = st.text_input("Contact Number", placeholder="Enter Contact No.", key="contact_val")

st.divider()


if st.button("🚀 Register Now", use_container_width=True):
    if con_name and category:
        if client:
            try:
                sheet = client.open("DWCS TWT").worksheet("Contractors")
                
                try:
                    header_cell = sheet.find("NAME OF CONTRACTOR")
                    header_row = header_cell.row
                except:
                    header_row = 1

                # લોજિક ચેક
                l_type1 = "Skill" if st.session_state.skill_check_val else ""
                l_type2 = "Unskill" if st.session_state.unskill_check_val else ""
                s_rate = skill_rate if st.session_state.skill_check_val else "0"
                u_rate = unskill_rate if st.session_state.unskill_check_val else "0"

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

                sheet.insert_row(data_to_save, index=header_row + 1, value_input_option='USER_ENTERED')

                # ડેટા ક્લિયર કરવા માટે સેશન સ્ટેટ અપડેટ
                st.session_state.con_name_val = ""
                st.session_state.category_val = ""
                st.session_state.location_val = ""
                st.session_state.contact_val = ""
                st.session_state.s_rate_val = "0"
                st.session_state.u_rate_val = "0"
                st.session_state.skill_check_val = False
                st.session_state.unskill_check_val = False
                
                st.success(f"✅ {con_name} Registered Successfully!")
                st.balloons()
                
                # પેજ રીફ્રેશ કરવું જરૂરી છે
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Connection Failed!")
    else:
        st.warning("Please fill Contractor Name and Category.")