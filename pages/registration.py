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
            padding-top: 2rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
            } 
            /* Background Color Same Like Mobile App */
            .stApp {
                background-color: #f0f2f6;
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

st.title("Contractor Registration")

