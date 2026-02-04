
import streamlit as st
from connection import get_gspread_client
import datetime

#a Line USe karvi varmvar raun Nahi thay
@st.cache_resource(show_spinner="Connecting to Database...")
def check_connection():
    try:
       client = get_gspread_client()
       sheet = client.open("DWCS TWT").worksheet("Contractors")
       return True, "Connected to Database successfully!"
    except Exception as e:
       return False, f"Connection failed: {e}"
is_connected,msg = check_connection()

if is_connected and 'connected_shown' not in st.session_state:
    st.session_state.connected_shown = True
    st.toast(msg, icon="✅")    
elif not is_connected:
    st.error(msg)
    st.info("Please check your Google Cloud credentials and internet connection.")

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
        
        #1. table na Badha j record leshe header Mujab
        # Sheet ma Niche Navu table Hashe to vadho Nahi ave
        all_records = sheet.get_all_records()
        
        #2.Duplicate Vender Code Check karvo
        new_code = str(st.session_state.get("con_vendercode")).strip()
        
        #3list comprehension thi duplicate code check karvo
        is_Duplicate = any(str(record.get("Vender Code")).strip() == str(new_code) for record in all_records)
        
        if is_Duplicate:
            st.warning(f"Vender Code {new_code} already exists. Please use a unique Vender Code.")
            return False
        
        labour_1 ="SKILL" if st.session_state.get("skill_Check") else ""
        labour_2 ="UNSKILL" if st.session_state.get("unskill_Check") else ""
        s_rate = st.session_state.get("skill_rate") if st.session_state.get("skill_Check") and st.session_state.get("skill_rate") != 0 else ""
        u_rate = st.session_state.get("unskill_rate") if st.session_state.get("unskill_Check") and st.session_state.get("unskill_rate") != 0 else ""
        new_row = [
            datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), 
            new_code,
            st.session_state.get("con_sitename", "").upper().strip(),
            st.session_state.get("con_Billname", "").upper().strip(),
            st.session_state.get("con_worktype", "").upper().strip(),
            st.session_state.get("con_cat", "").upper().strip(),
            labour_1, #'True' na badle 'Skill' or khali jagaya ma sae thasehe
            labour_2, #'True' na badle 'Unskill' or khali jagaya ma sae thasehe
            s_rate, # jo 0 hashe to ahi "" save thasehe
            u_rate # jo 0 hashe to ahi "" save thasehe
        ]
        # VBA na Rows(2).Insert logic jevu kaam:
        # Aa command 2nd number ni row (Header ni turant niche) navi row umero ane data muko
        sheet.insert_row(new_row, index=2, value_input_option='USER_ENTERED')
        return True
    except Exception as e:
        st.error(f"Error saving data to Google Sheets: {e}")
        return False    
    



with tab1:
    #--- This is Ractangle Box (Card) ---
    with st.container(border=True): 
        con_vendercode = st.number_input("Contractor Vender Code*",key="con_vendercode", placeholder="Enter Contractor Vender Code")
        col1,col2 = st.columns([1,1])
        with col1:
             con_sitename = st.text_input("Contractor Site Name*",key="con_sitename", placeholder="Enter Contractor Site Name")
        with col2:
            con_Billname = st.text_input("Contractor Bill Name",key="con_Billname", placeholder="Enter Contractor Bill Name")
        work_Option =["Regular","Naka"]
        con_worktype = st.selectbox("Contractor Work Type*",key="con_worktype", options=work_Option, index=None, help="Refular or Naka Work Type")
        category_Option =["Shuttering","Steel","Exposed and Rendering","Unskill","Concrete"]
        con_cat = st.selectbox("Contractor Category*",key="con_cat", options=category_Option, index=None, help="Select Category",placeholder="Select Category")
        col1, col2 = st.columns([1,2]) #[checkox ni jagya,Text box ni jagya]
        with col1:
            skill_check =st.checkbox("Skill",key="skill_Check")
        with col2:
            skill_rate = st.number_input("Skill Rate*",key="skill_rate", min_value=0.0, format="%.2f", step=0.50,disabled=not skill_check, placeholder="Enter Skill Rate")
        col3, col4 = st.columns([1,2]) #[checkox ni jagya,Text box ni jagya]
        with col3:
            unskill_check =st.checkbox("Unskill",key="unskill_Check")
        with col4:
            unskill_rate = st.number_input("Unskill Rate*",key="unskill_rate", min_value=0.0, format="%.2f", step=0.50,disabled=not unskill_check, placeholder="Enter Unskill Rate")
 #1 Ragister Button           
if st.button("Register Contractor",use_container_width=True):
    #2 Validation for Required Fields
    if not st.session_state.get("con_vendercode") or not st.session_state.get("con_sitename") or not st.session_state.get("con_worktype") or not st.session_state.get("con_cat"):
        st.error("Please fill all required fields in Basic Details.")
    else:
    #3 Loding Message
        with st.spinner("All Data Save in DataBase..."):
            is_saved = save_contractor_smart()
            if is_saved:
                st.write(st.session_state.to_dict()) # આનાથી બધી વેલ્યુ સ્ક્રીન પર દેખાશે     
                st.success(f"Contractor {st.session_state.get('con_sitename')} Registered Successfully!")
                st.balloons()
            else:
                st.error("Failed to register contractor. Please try again.")  