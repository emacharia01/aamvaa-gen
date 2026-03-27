import streamlit as st
from datetime import date
import random

# 1. Page Config
st.set_page_config(page_title="WA State AAMVA Generator", page_icon="🪪", layout="wide")

st.title("🪪 Washington State DL Generator")
st.caption("v6.0 - Full WA-Spec: Includes Compliance and Truncation Fields")

# 2. Escape Constants
LF, RS, CR = "\\n", "\\x1E", "\\r"

def generate_wa_dl():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "WDL" + ''.join(random.choice(chars) for _ in range(9))

# 3. UI Inputs
col1, col2 = st.columns(2)
with col1:
    dl_number = st.text_input("Customer ID (DAQ)", value=generate_wa_dl())
    first_name = st.text_input("First Name (DAC)", "ISAAC")
    middle_name = st.text_input("Middle Name (DAD)", "A")
    last_name = st.text_input("Last Name (DCS)", "HUTCHISON")
    address = st.text_input("Address (DAG)", "23702 110TH AVE SE")
    city = st.text_input("City (DAI)", "KENT")
    zipcode = st.text_input("Zip (DAK)", "993235460")

with col2:
    dob = st.date_input("Date of Birth (DBB)", date(1977, 12, 16))
    expiry = st.date_input("Expiry Date (DBA)", date(2027, 12, 16))
    issue = st.date_input("Issue Date (DBD)", date(2022, 1, 22))
    height = st.number_input("Height (inches)", value=67)
    compliance = st.selectbox("Compliance Type (DDA)", ["N", "F"])
    eye_color = st.selectbox("Eye Color (DAY)", ["BLK", "BRO", "BLU"])

# 4. Generate WA-Spec String
if st.button("Generate WA-Spec String", type="primary", use_container_width=True):
    
    # Washington-Specific Field Order & Data
    fields = [
        ("DAC", first_name.upper()),
        ("DCS", last_name.upper()),
        ("DAD", middle_name.upper()),
        ("DCA", "D"),
        ("DCB", "NONE"),
        ("DCD", "NONE"),
        ("DBA", expiry.strftime("%m%d%Y")),
        ("DBB", dob.strftime("%m%d%Y")),
        ("DBD", issue.strftime("%m%d%Y")),
        ("DDA", compliance),           # Added: Compliance Type
        ("DBC", "1"),
        ("DAY", eye_color),
        ("DAU", f"{height:03d} in"),
        ("DAG", address.upper()),
        ("DAI", city.upper()),
        ("DAJ", "WA"),
        ("DAK", zipcode),
        ("DAQ", dl_number),
        ("DCF", f"{dl_number}S012225H1784"),
        ("DCG", "USA"),
        ("DDE", "N"),                 # Added: Family name truncation
        ("DDF", "N"),                 # Added: First name truncation
        ("DDG", "N"),                 # Added: Middle name truncation
        ("DCJ", "S012225H1784"),      # Audit Info
        ("DDB", "11122019"),          # Added: WA Standard Revision Date
        ("DAW", "148"),
        ("DDK", "1")
    ]

    data_body = "".join(f"{LF}{code}{value}" for code, value in fields)
    subfile_content = f"DL{data_body}{LF}"
    total_bytes = len(subfile_content)
    
    # Header with Auto-Length
    header = f"@{LF}{RS}{CR}ANSI 636045080001DL0041{total_bytes:04d}"
    final_string = f"{header}{subfile_content}ZVA01{CR}"

    st.subheader("📋 Copy for TEC-IT")
    st.text_area(label="WA-Spec Result", value=final_string, height=250)
    st.success("Tweak Complete: Compliance, Truncations, and WA-Revision Date included.")

st.info("💡 **Pro-Tip:** If you use the full middle name 'NGANGA', the parser will now show it correctly under 'Customer Middle Name(s)'.")