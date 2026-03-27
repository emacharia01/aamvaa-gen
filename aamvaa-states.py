import streamlit as st
from datetime import date

st.set_page_config(page_title="Universal AAMVA Generator", layout="wide")
st.title("🌎 Universal AAMVA Generator (All-States)")

# 1. State Selector
selected_state_code = st.selectbox("Select Jurisdiction", list(STATES.keys()), format_func=lambda x: f"{x} - {STATES[x]['name']}")
PROFILE = STATES[selected_state_code]

# 2. User Inputs
col1, col2 = st.columns(2)
with col1:
    first = st.text_input("First Name (DAC)", "JAMES")
    middle = st.text_input("Middle Name (DAD)", "A")
    last = st.text_input("Last Name (DCS)", "SMITH")
    
    # Auto-Generate DLN based on State Rules
    if PROFILE["dln_mode"] == "SOUNDEX":
        # Placeholder dob/gender for initial load
        dln_preview = "(Auto-Calculated from Name/DOB)"
    else:
        dln_preview = get_random_dln(PROFILE["dln_pattern"])
        
    dln_input = st.text_input(f"License Number (DAQ) - {PROFILE['dln_mode']}", value=dln_preview)
    
    address = st.text_input("Address (DAG)", "123 MAIN ST")
    city = st.text_input("City (DAI)", "ANYTOWN")
    zipcode = st.text_input("Zip (DAK)", "90210")

with col2:
    dob = st.date_input("Date of Birth (DBB)", date(1985, 5, 15))
    gender = st.selectbox("Sex (DBC)", ["1", "2"], format_func=lambda x: "Male (1)" if x=="1" else "Female (2)")
    
    # Recalculate DLN if Soundex
    if PROFILE["dln_mode"] == "SOUNDEX":
        calculated_dln = generate_coded_dln(selected_state_code, last, first, middle, dob, gender)
        st.info(f"🧮 Calculated DLN: {calculated_dln}")
        final_dln = calculated_dln
    else:
        final_dln = dln_input

    issue = st.date_input("Issue Date (DBD)", date(2023, 1, 10))
    expiry = st.date_input("Expiry Date (DBA)", date(2028, 1, 10))
    eyes = st.selectbox("Eyes (DAY)", ["BRO", "BLU", "BLK", "GRN"])
    height = st.text_input("Height (DAU)", "070 in")

# 3. Document Discriminator Logic Engine
def generate_discriminator(state_code, dln, issue_date):
    mode = STATES[state_code]["dd_mode"]
    issue_str = issue_date.strftime("%m%d%Y")
    
    if mode == "COMPOSITE_WA":
        # WA: ID + Office(O) + IssueDate + Seq
        return f"{dln}O{issue_str}12345"
    elif mode == "COMPOSITE_FL":
        # FL: Office + Date + Seq (FL doesn't put DLN in DD usually)
        return f"1234{issue_str}9999" 
    elif mode == "SERIAL_10": # NY
        return ''.join(random.choices("ABCDEF0123456789", k=10))
    elif mode == "SERIAL_12": # CA
        return ''.join(random.choices("ABCDEF0123456789", k=12))
    elif mode == "SERIAL_20": # TX
        return ''.join(random.choices("0123456789", k=20))
    elif mode == "SERIAL_16": # IL
        return ''.join(random.choices("0123456789", k=16))
    return f"{dln}{issue_str}" # Fallback

# 4. Generate
if st.button("Generate Universal String"):
    # Calculate Dynamic Fields
    dd_val = generate_discriminator(selected_state_code, final_dln, issue)
    
    # Define Fields
    fields = [
        ("DCA", "D"),
        ("DCB", "NONE"),
        ("DCD", "NONE"),
        ("DBA", expiry.strftime("%m%d%Y")),
        ("DCS", last.upper()),
        ("DAC", first.upper()),
        ("DAD", middle.upper()),
        ("DBD", issue.strftime("%m%d%Y")),
        ("DBB", dob.strftime("%m%d%Y")),
        ("DBC", gender),
        ("DAY", eyes),
        ("DAU", height),
        ("DAG", address.upper()),
        ("DAI", city.upper()),
        ("DAJ", selected_state_code), # Dynamic State
        ("DAK", zipcode),
        ("DAQ", final_dln), # Dynamic DLN
        ("DCF", dd_val),    # Dynamic Discriminator
        ("DCG", "USA"),
        ("DDE", "N"),
        ("DDF", "N"),
        ("DDG", "N"),
        # Logic: Most states use DCF as DCJ, except WA/CO
        ("DCJ", dd_val if selected_state_code != "WA" else dd_val[len(final_dln):]), 
        ("DDB", PROFILE["revision_date"]), # State-specific revision
        ("DDA", PROFILE["compliance"]),    # REAL ID Status
        ("DDK", "1")
    ]
    
    # Construct
    LF, RS, CR = "\\n", "\\x1E", "\\r"
    data_body = "".join(f"{LF}{k}{v}" for k, v in fields)
    subfile = f"DL{data_body}{LF}"
    
    # IIN Injection
    iin = PROFILE["iin"]
    header = f"@{LF}{RS}{CR}ANSI {iin}080001DL0041{len(subfile):04d}"
    
    final_string = f"{header}{subfile}ZVA01{CR}"
    
    st.subheader(f"✅ {PROFILE['name']} AAMVA String")
    st.text_area("Result", final_string, height=250)
    st.success(f"Applied Rules: IIN={iin} | DLN={PROFILE['dln_mode']} | DD={PROFILE['dd_mode']}")