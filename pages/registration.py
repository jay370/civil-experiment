import streamlit as st

st.set_page_config(page_title="Registration", layout="centered")

st.title("Registration Form")

with st.form("registration_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    submitted = st.form_submit_button("Register")
    
    if submitted:
        if name and email and password:
            st.success(f"Welcome {name}! Registration successful.")
        else:
            st.error("Please fill in all fields.")