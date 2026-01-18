import streamlit as st

# page setup for Mobile Look
st.set_page_config(page_title="Contractor Registration", layout="centered",initial_sidebar_state="collapsed")

# css For styling of Page

st.markdown("""
    <style>
            /* Top Lal Bar Remove */
            MainMenu {visibility: hidden;}
            Header {visibility: hidden;}
            footer {visibility: hidden;}

            /* Remove Page Padding */
            .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0.0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            } 
            /* Background Color Same Like Mobile App */
            .stApp {
                background-color: #007AFF;
            }
            /* Ragister Button-feel  like Apple Button */
            .stButton>button {
                background-color: #007aff;
                color: #ffffff;
                border-radius: 12px;
                height: 50px;
                width: 100%;
                font-size: 1.2em;
                font-weight: bold;
                box-shadow: 0px 4px 12px rgba(0, 122, 255, 0, 0.3);
                border: none;

            }
</style> """, unsafe_allow_html=True)

st.markdown("""
            <h2 style="text-align: center; 
            color: #28A745;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 800;
            background-color: #ffffff;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 1);
            border-bottom: 5px solid #007aff;
            ">Contractor Registration</h2>
""", unsafe_allow_html=True)
