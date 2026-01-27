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
            /*Rectangle Box (card) ni style */
            div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            border: none !important;
            margin-bottom: 20px;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
            gap: 0.1rem !important;
            }
            /*Lable and box vache ni space control */
            div[data-testid="stwidgetLabel"] p{
            margin-bottom: -20px !important;
            font-size: 16px;
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
            font-size: 25px;
            font-weight: 800;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
            border-bottom: 5px solid #007aff;
            ">Contractor Registration</h2>
""", unsafe_allow_html=True)



#-- Tabs for Input Fields --
tab1, tab2 = st.tabs(["Basic Details", "Bank Details"])

with tab1:
    #--- This is Ractangle Box (Card) ---
    with st.container(border=True): 
        con_sitename = st.text_input("Contractor Site Name*",key="con_sitename", placeholder="Enter Contractor Site Name")
        work_Option =["Regular","Naka"]
        con_worktype = st.selectbox("Contractor Work Type*",key="con_worktype", options=work_Option, index=None, help="Refular or Naka Work Type")
        category_Option =["Shuttering","Steel","Exposed and Rendering","Unskill","Concrete"]
        con_cat = st.selectbox("Contractor Category*",key="con_cat", options=category_Option, index=None, help="Select Category",placeholder="Select Category")
        col1, col2 = st.columns([1,2]) #[checkox ni jagya,Text box ni jagya]
        with col1:
            skill_check =st.checkbox("Skill",key="skill_Check")
        with col2:
            skill_rate = st.number_input("Skill Rate*",key="skill_rate", min_value=0.0, format="%.2f", step=0.50,disabled=not skill_check, placeholder="Enter Skill Rate")
        with col3:
            unskill_check =st.checkbox("Unskill",key="unskill_Check")
        with col2:
            unskill_rate = st.number_input("Unskill Rate*",key="unskill_rate", min_value=0.0, format="%.2f", step=0.50,disabled=not unskill_check, placeholder="Enter Unskill Rate")
with tab2:
    st.markdown("### Register Contractor Bank Details")

