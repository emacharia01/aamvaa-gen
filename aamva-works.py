import streamlit as st
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="Universal AAMVA Master", page_icon="🌎", layout="wide")
st.title("🌎 Universal AAMVA Master System")
st.caption("v14.0 - Full 68-Jurisdiction Database | Complete Manual Entry Suite")

# --- 2. FULL MASTER IIN DATABASE (68 JURISDICTIONS) ---
MASTER_DB = {
    # US STATES & DC (your existing database - unchanged)
    "AL": {"iin": "636033", "name": "Alabama"}, "AK": {"iin": "636059", "name": "Alaska"},
    "AZ": {"iin": "636026", "name": "Arizona"}, "AR": {"iin": "636021", "name": "Arkansas"},
    "CA": {"iin": "636014", "name": "California"}, "CO": {"iin": "636020", "name": "Colorado"},
    "CT": {"iin": "636006", "name": "Connecticut"}, "DE": {"iin": "636011", "name": "Delaware"},
    "DC": {"iin": "636043", "name": "District of Columbia"}, "FL": {"iin": "636010", "name": "Florida"},
    "GA": {"iin": "636055", "name": "Georgia"}, "HI": {"iin": "636047", "name": "Hawaii"},
    "ID": {"iin": "636050", "name": "Idaho"}, "IL": {"iin": "636035", "name": "Illinois"},
    "IN": {"iin": "636037", "name": "Indiana"}, "IA": {"iin": "636018", "name": "Iowa"},
    "KS": {"iin": "636022", "name": "Kansas"}, "KY": {"iin": "636046", "name": "Kentucky"},
    "LA": {"iin": "636007", "name": "Louisiana"}, "ME": {"iin": "636041", "name": "Maine"},
    "MD": {"iin": "636003", "name": "Maryland"}, "MA": {"iin": "636002", "name": "Massachusetts"},
    "MI": {"iin": "636032", "name": "Michigan"}, "MN": {"iin": "636038", "name": "Minnesota"},
    "MS": {"iin": "636051", "name": "Mississippi"}, "MO": {"iin": "636030", "name": "Missouri"},
    "MT": {"iin": "636008", "name": "Montana"}, "NE": {"iin": "636054", "name": "Nebraska"},
    "NV": {"iin": "636049", "name": "Nevada"}, "NH": {"iin": "636039", "name": "New Hampshire"},
    "NJ": {"iin": "636036", "name": "New Jersey"}, "NM": {"iin": "636009", "name": "New Mexico"},
    "NY": {"iin": "636001", "name": "New York"}, "NC": {"iin": "636004", "name": "North Carolina"},
    "ND": {"iin": "636034", "name": "North Dakota"}, "OH": {"iin": "636023", "name": "Ohio"},
    "OK": {"iin": "636058", "name": "Oklahoma"}, "OR": {"iin": "636029", "name": "Oregon"},
    "PA": {"iin": "636025", "name": "Pennsylvania"}, "RI": {"iin": "636052", "name": "Rhode Island"},
    "SC": {"iin": "636005", "name": "South Carolina"}, "SD": {"iin": "636042", "name": "South Dakota"},
    "TN": {"iin": "636053", "name": "Tennessee"}, "TX": {"iin": "636015", "name": "Texas"},
    "UT": {"iin": "636040", "name": "Utah"}, "VT": {"iin": "636024", "name": "Vermont"},
    "VA": {"iin": "636000", "name": "Virginia"}, "WA": {"iin": "636045", "name": "Washington"},
    "WV": {"iin": "636061", "name": "West Virginia"}, "WI": {"iin": "636030", "name": "Wisconsin"},
    "WY": {"iin": "636060", "name": "Wyoming"},
    # US TERRITORIES & CANADA (unchanged)
    "AS": {"iin": "604427", "name": "American Samoa"}, "GU": {"iin": "636019", "name": "Guam"},
    "MP": {"iin": "604430", "name": "Northern Mariana Islands"}, "PR": {"iin": "604431", "name": "Puerto Rico"},
    "VI": {"iin": "636062", "name": "U.S. Virgin Islands"},
    "AB": {"iin": "604432", "name": "Alberta"}, "BC": {"iin": "636028", "name": "British Columbia"},
    "MB": {"iin": "636031", "name": "Manitoba"}, "NB": {"iin": "636013", "name": "New Brunswick"},
    "NL": {"iin": "636027", "name": "Newfoundland and Labrador"}, "NS": {"iin": "636017", "name": "Nova Scotia"},
    "ON": {"iin": "636012", "name": "Ontario"}, "PE": {"iin": "636016", "name": "Prince Edward Island"},
    "QC": {"iin": "604428", "name": "Quebec"}, "SK": {"iin": "636031", "name": "Saskatchewan"}
}

# --- 3. UI LAYOUT ---
selected_abbr = st.selectbox("Select Jurisdiction", sorted(list(MASTER_DB.keys())), 
                             format_func=lambda x: f"{x} - {MASTER_DB[x]['name']}")
iin = MASTER_DB[selected_abbr]["iin"]

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 👤 Personal Identity")
    f_name = st.text_input("First Name (DAC)", "ethan")
    m_name = st.text_input("Middle Name (DAD)", "james")
    l_name = st.text_input("Last Name (DCS)", "macharia")
    suffix = st.text_input("Suffix (DCU)", "")
    
    # No year limit for Date of Birth
    dob = st.date_input("Date of Birth (DBB)", 
                        value=date(1977, 12, 16),
                        min_value=date(1900, 1, 1),   # You can change or remove this
                        max_value=date(2100, 12, 31)) # You can change or remove this

    gender = st.selectbox("Sex (DBC)", ["Male (1)", "Female (2)"])
    race = st.text_input("Race / Ethnicity (DCL)", "bk")
    ssn = st.text_input("Social Security Num (DBK)", "")

with col2:
    st.markdown("### 📍 Location & Physicals")
    addr = st.text_input("Street 1 (DAG)", "6517 deer horn dr")
    city = st.text_input("City (DAI)", "fort worth")
    zipc = st.text_input("Postal Code (DAK)", "76179")
    country = st.text_input("Country (DCG)", "usa")
    height = st.text_input("Height (DAU)", "067 in")
    weight_lb = st.text_input("Weight lbs (DAW)", "148")
    weight_kg = st.text_input("Weight kg (DAX)", "")
    eyes = st.text_input("Eye Color (DAY)", "bro")
    hair = st.text_input("Hair Color (DAZ)", "blk")

with col3:
    st.markdown("### 💳 Document Security")
    dln = st.text_input("Customer ID (DAQ)", "40534413")
    dd_val = st.text_input("Document Discriminator (DCF)", "06629180138093952956")
    audit = st.text_input("Inventory Control / Audit (DCJ)", "10006088295")
    
    # No year limit for Issue Date
    iss_date = st.date_input("Issue Date (DBD)", 
                             value=date(2022, 1, 22),
                             min_value=date(1900, 1, 1),
                             max_value=date(2100, 12, 31))
    
    # No year limit for Expiry Date
    exp_date = st.date_input("Expiry Date (DBA)", 
                             value=date(2027, 12, 16),
                             min_value=date(1900, 1, 1),
                             max_value=date(2100, 12, 31))
    
    rev_date = st.text_input("Card Revision Date (DDB)", "11122019")
    compliance = st.text_input("Compliance Type (DDA)", "n")
    
    st.markdown("### 🚦 Authorization Codes")
    v_class = st.text_input("Vehicle Class (DCA)", "c")
    restr = st.text_input("Restrictions (DCB)", "NONE")
    endors = st.text_input("Endorsements (DCD)", "NONE")
    donor = st.text_input("Organ Donor (DDK)", "1")

# --- 4. GENERATION LOGIC ---
if st.button("Generate Master AAMVA String", type="primary", use_container_width=True):
    
    fields = [
        ("DAC", f_name.upper()), ("DCS", l_name.upper()), ("DAD", m_name.upper()),
        ("DCU", suffix.upper()), ("DBB", dob.strftime("%m%d%Y")),
        ("DBA", exp_date.strftime("%m%d%Y")), ("DBD", iss_date.strftime("%m%d%Y")),
        ("DAU", height), ("DAY", eyes.upper()), ("DAZ", hair.upper()),
        ("DAW", weight_lb), ("DAX", weight_kg),
        ("DBC", gender[-2] if len(gender) > 1 else gender),
        ("DCL", race.upper()), ("DBK", ssn),
        ("DAG", addr.upper()), ("DAI", city.upper()),
        ("DAJ", selected_abbr), ("DAK", zipc), ("DCG", country.upper()),
        ("DAQ", dln.upper()), ("DCF", dd_val.upper()), ("DCJ", audit.upper()),
        ("DDA", compliance.upper()), ("DDB", rev_date), ("DDK", donor),
        ("DCA", v_class.upper()), ("DCB", restr.upper()), ("DCD", endors.upper()),
        ("DDE", "N"), ("DDF", "N"), ("DDG", "N")
    ]

    LF, RS, CR = "\\n", "\\x1E", "\\r"
    
    data_body = "".join(f"{LF}{code}{val}" for code, val in fields if val)
    sub = f"DL{data_body}{LF}"
    
    header = f"@{LF}{RS}{CR}ANSI {iin}080001DL0045{len(sub):04d}"
    final_string = f"{header}{sub}ZVA01{CR}"

    st.divider()
    st.markdown("### 📋 Final String for TEC-IT")
    st.text_area("Result", value=final_string, height=250)
    st.success(f"Generated for {MASTER_DB[selected_abbr]['name']} (IIN: {iin}) with all credentials.")