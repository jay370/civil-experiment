import streamlit as st

def show_registration():
    st.subheader("Contractor Registration")
    st.write("Please fill in the details below to register as a contractor.")
    name = st.text_input("Contractor Name")
    agency = st.text_input("Agency Name")
    if st.button("Save Contractor"):
        st.success(f"Contractor {name} from {agency} registered successfully!")