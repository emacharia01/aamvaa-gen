import streamlit as st
import random
import string
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="Universal AAMVA Master", page_icon="🌎", layout="wide")
st.title("🌎 Universal AAMVA Master System")
st.caption("v7.0 - Complete 54-Jurisdiction Database | All AAMVA Data Elements")

# --- FULL JURISDICTION IIN DATABASE ---
IIN_DB = {
    "AL": "636000", "AK": "636033", "AZ": "636026", "AR": "636021", "CA": "636014", 
    "CO": "636006", "CT": "636007", "DE": "636011", "DC": "636049", "FL": "636010", 
    "GA": "636059", "HI": "636028", "ID": "636015", "IL": "636035", "IN": "636037", 
    "IA": "636016", "KS": "636017", "KY": "636018", "LA": "636019", "ME": "636051", 
    "MD": "636003", "MA": "636002", "MI": "636036", "MN": "636038", "MS": "636039", 
    "MO": "636040", "MT": "636041", "NE": "636042", "NV": "636022", "NH": "636043", 
    "NJ": "636004", "NM": "636044", "NY": "636001", "NC": "636005", "ND": "636046", 
    "OH": "636021", "OK": "636048", "OR": "636024", "PA": "636025", "RI": "636053", 
    "SC": "636054", "SD": "636055", "TN": "636056", "TX": "636020", "UT": "636029", 
    "VT": "636058", "VA": "636027", "WA": "636045", "WV": "636060", "WY": "636061",
    "PR": "636000", "GU": "636000", "VI": "636000", "AS": "636000", "MP": "636000"
}

# --- UI LAYOUT ---
selected_state = st.selectbox("Select Jurisdiction (DAJ)", sorted(list(IIN_DB.keys())))
iin = IIN_DB[selected_state]

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Personal Identity")
    f_name = st.text_input("First Name (DAC)", "ISAAC")
    m_name = st.text_input("Middle Name (DAD)", "NGANGA")
    l_name = st.text_input("Last Name (DCS)", "HUTCHISON")
    suffix = st.text_input("Suffix (DCU)", "3RD")
    dob = st.date_input("Date of Birth (DBB)", date(1977, 12, 16))
    gender = st.selectbox("Sex (DBC)", ["1", "2"], format_func=lambda x: "Male (1)" if x=="1" else "Female (2)")
    race = st.text_input("Race / Ethnicity (DCL)", "B")
    ssn = st.text_input("Social Security Num (DBK)", "")

with col2:
    st.subheader("📍 Location & Physicals")
    addr = st.text_input("Street 1 (DAG)", "23702 110TH AVE SE")
    city = st.text_input("City (DAI)", "KENT")
    zipc = st.text_input("Postal Code (DAK)", "993235460")
    country = st.text_input("Country (DCG)", "USA")
    eyes = st.text_input("Eye Color (DAY)", "BLK")
    hair = st.text_input("Hair Color (DAZ)", "BLK")
    height = st.text_input("Height (DAU)", "067 in")
    weight_lb = st.text_input("Weight lbs (DAW)", "148")
    weight_kg = st.text_input("Weight kg (DAX)", "")

with col3:
    st.subheader("💳 Document Security")
    dln = st.text_input("Customer ID (DAQ)", "WDLGJL7I0OB2")
    dd_val = st.text_input("Document Discriminator (DCF)", "WDLGJL7I0OB2S012225H1784")
    audit = st.text_input("Audit Information (DCJ)", "S012225H1784")
    iss_date = st.date_input("Issue Date (DBD)", date(2022, 1, 22))
    exp_date = st.date_input("Expiry Date (DBA)", date(2027, 12, 16))
    rev_date = st.text_input("Card Revision Date (DDB)", "11122019")
    compliance = st.text_input("Compliance Type (DDA)", "N")
    
    st.subheader("🚦 Authorization Codes")
    v_class = st.text_input("Vehicle Class (DCA)", "D")
    restr = st.text_input("Restrictions (DCB)", "NONE")
    endors = st.text_input("Endorsements (DCD)", "NONE")
    donor = st.text_input("Organ Donor (DDK)", "1")

# --- GENERATION LOGIC ---
if st.button("Generate Master AAMVA String", type="primary", use_container_width=True):
    
    # 1. Map all AAMVA standard codes
    fields = [
        ("DAC", f_name.upper()),
        ("DCS", l_name.upper()),
        ("DAD", m_name.upper()),
        ("DCU", suffix.upper()),
        ("DBB", dob.strftime("%m%d%Y")),
        ("DBA", exp_date.strftime("%m%d%Y")),
        ("DBD", iss_date.strftime("%m%d%Y")),
        ("DAU", height),
        ("DAY", eyes.upper()),
        ("DAZ", hair.upper()),
        ("DAW", weight_lb),
        ("DAX", weight_kg),
        ("DBC", gender),
        ("DCL", race.upper()),
        ("DBK", ssn),
        ("DAG", addr.upper()),
        ("DAI", city.upper()),
        ("DAJ", selected_state),
        ("DAK", zipc),
        ("DCG", country.upper()),
        ("DAQ", dln.upper()),
        ("DCF", dd_val.upper()),
        ("DCJ", audit.upper()),
        ("DDA", compliance.upper()),
        ("DDB", rev_date),
        ("DDK", donor),
        ("DCA", v_class.upper()),
        ("DCB", restr.upper()),
        ("DCD", endors.upper()),
        # Truncation flags: N = Not truncated
        ("DDE", "N"), ("DDF", "N"), ("DDG", "N")
    ]

    # 2. String Assembly (Byte-Perfect for BarKoder)
    LF, RS, CR = "\\n", "\\x1E", "\\r"
    
    # Data subfile content
    data_body = "".join(f"{LF}{code}{val}" for code, val in fields if val)
    subfile = f"DL{data_body}{LF}"
    
    # Header: IIN + Version 08 + Offset 0045 + Calculated Length
    header = f"@{LF}{RS}{CR}ANSI {iin}080001DL0045{len(subfile):04d}"
    
    final_string = f"{header}{subfile}ZVA01{CR}"

    # 3. Final Output
    st.divider()
    st.subheader("📋 Final String for TEC-IT")
    st.text_area("Result", value=final_string, height=280)
    st.success(f"Jurisdiction {selected_state} (IIN {iin}) ready.")