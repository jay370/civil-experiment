import streamlit as st
from connection import get_gspread_client # connection.py mathi lyo

# --- 1. CONFIGURATION (Fakt ahiya j hovvi joie) ---
st.set_page_config(page_title="Civil Site App", layout="centered")

# --- 2. DATABASE CONNECTION ---
client = get_gspread_client()

# --- 3. HOME UI ---
st.title("🏗️ Civil Site Home Page")
st.write("Welcome! Use the sidebar or button below.")

# Navigation Button
if st.button("Contractor Registration Page par jao"):
    # Pages folder mate sacho path
     st.switch_page("pages/registration.py")

if client:
    st.sidebar.success("Database Connected ✅")
else:
    st.sidebar.error("Database Connection Failed ❌")