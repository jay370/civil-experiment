import streamlit as st
from connection import get_gspread_client
import datetime

# --- Form Reset Logic (Top Level) ---
if "form_version" not in st.session_state:
    st.session_state.form_version = 0

# a Line USe karvi varmvar raun Nahi thay
@st.cache_resource(show_spinner="Connecting to Database...")
def check_connection():
    try:
        client = get_gspread_client()
        sheet = client.open("DWCS TWT").worksheet("Contractors")
        return True, "Connected to Database successfully!"
    except Exception as e:
        return False, f"Connection failed: {e}"

is_connected, msg = check_connection()

if is_connected and 'connected_shown' not in st.session_state:
    st.session_state.connected_shown = True
    st.toast(msg, icon="✅")    
elif not is_connected:
    st.error(msg)
    st.info("Please check your Google Cloud credentials and internet connection.")

# page setup for Mobile Look
st.set_page_config(page_title="Contractor Registration", layout="centered", initial_sidebar_state="collapsed")

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
            /*Number Inpute Box +/- Button Hide*/
            button[step="1"] {
                display: none !important;
            }
            input[type="number"]::-webkit-inner-spin-button,
            input[type="number"]::-webkit-outer-spin-button {
                -webkit-appearance: none;
                margin: 0 !important;
            }
            input[type="number"] {
                -moz-appearance: textfield !important;
            }
            [data-testid="column"] {
                width: unset !important;
                flex:1 1 0% !important;
                min-width: 0px !important;
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

def save_contractor_smart():
    try:
        client = get_gspread_client()
        sheet = client.open("DWCS TWT").worksheet("Contractors")  # Sheet name
        
        # 1. table na Badha j record leshe header Mujab
        all_records = sheet.get_all_records()
        
        # 2. Duplicate Vender Code Check karvo (Current Version Key sathe)
        ver = st.session_state.form_version
        new_code = str(st.session_state.get(f"vcode_{ver}"))
        
        # 3. list comprehension thi duplicate code check karvo
        is_Duplicate = any(str(record.get("Vender Code", "")) == str(new_code) for record in all_records)
        
        if is_Duplicate:
            st.warning(f"Vender Code {new_code} already exists. Please use a unique Vender Code.")
            return False
        
        labour_1 = "SKILL" if st.session_state.get(f"skill_chk_{ver}") else ""
        labour_2 = "UNSKILL" if st.session_state.get(f"unskill_chk_{ver}") else ""
        
        s_rate = st.session_state.get(f"s_rate_{ver}") if st.session_state.get(f"skill_chk_{ver}") and st.session_state.get(f"s_rate_{ver}") != 0 else ""
        u_rate = st.session_state.get(f"u_rate_{ver}") if st.session_state.get(f"unskill_chk_{ver}") and st.session_state.get(f"u_rate_{ver}") != 0 else ""
        
        new_row = [
            datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), 
            new_code,
            st.session_state.get(f"site_{ver}", "").upper().strip(),
            st.session_state.get(f"bill_{ver}", "").upper().strip(),
            st.session_state.get(f"wtype_{ver}", "").upper().strip() if st.session_state.get(f"wtype_{ver}") else "",
            st.session_state.get(f"cat_{ver}", "").upper().strip() if st.session_state.get(f"cat_{ver}") else "",
            labour_1,
            labour_2,
            s_rate,
            u_rate
        ]
        
        sheet.insert_row(new_row, index=2, value_input_option='USER_ENTERED')
        return True
    except Exception as e:
        st.error(f"Error saving data to Google Sheets: {e}")
        return False    

with tab1:
    ver = st.session_state.form_version
    #--- This is Ractangle Box (Card) ---
    with st.container(border=True): 
        st.number_input("Contractor Vender Code*", key=f"vcode_{ver}", placeholder="Enter Contractor Vender Code")
        col1, col2 = st.columns([1,1])
        with col1:
             st.text_input("Contractor Site Name*", key=f"site_{ver}", placeholder="Enter Contractor Site Name")
        with col2:
            st.text_input("Contractor Bill Name", key=f"bill_{ver}", placeholder="Enter Contractor Bill Name")
        
        work_Option = ["Regular", "Naka"]
        st.selectbox("Contractor Work Type*", key=f"wtype_{ver}", options=work_Option, index=None, help="Regular or Naka Work Type")
        
        category_Option = ["Shuttering", "Steel", "Exposed and Rendering", "Unskill", "Concrete"]
        st.selectbox("Contractor Category*", key=f"cat_{ver}", options=category_Option, index=None, help="Select Category", placeholder="Select Category")
        
        col1, col2 = st.columns([1,2])
        with col1:
            st.checkbox("Skill", key=f"skill_chk_{ver}")
        with col2:
            st.number_input("Skill Rate*", key=f"s_rate_{ver}", min_value=0.0, format="%.2f", step=0.50, disabled=not st.session_state.get(f"skill_chk_{ver}"), placeholder="Enter Skill Rate")
        
        col3, col4 = st.columns([1,2])
        with col3:
            st.checkbox("Unskill", key=f"unskill_chk_{ver}")
        with col4:
            st.number_input("Unskill Rate*", key=f"u_rate_{ver}", min_value=0.0, format="%.2f", step=0.50, disabled=not st.session_state.get(f"unskill_chk_{ver}"), placeholder="Enter Unskill Rate")

# 1 Register Button           
    if st.button("Register Contractor", use_container_width=True):
    ver = st.session_state.form_version
    # 2 Validation for Required Fields
    if not st.session_state.get(f"vcode_{ver}") or not st.session_state.get(f"site_{ver}") or not st.session_state.get(f"wtype_{ver}") or not st.session_state.get(f"cat_{ver}"):
        st.error("Please fill all required fields in Basic Details.")
    else:
        # 3 Loding Message
        with st.spinner("All Data Save in DataBase..."):
            is_saved = save_contractor_smart()
            if is_saved:
                st.success(f"Contractor Registered Successfully!")
                st.balloons()
                # Form Reset Logic: Version badlvathi badha box khali thai jashe
                st.session_state.form_version += 1
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to register contractor. Please try again.")  

    # ૧. Reset બટન (બધા ખાના ખાલી કરવા માટે)
    if st.button("Reset Form", use_container_width=True):
    # Version badlvathi Streamlit badha widget ne nava ganashe ane khali kari deshe
        st.session_state.form_version += 1
        st.rerun()