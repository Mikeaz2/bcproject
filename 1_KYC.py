import streamlit as st
from datetime import datetime

st.set_page_config(page_title="KYC – BC", page_icon="🪪", layout="wide")
st.title("KYC / Identity Verification (Simulated)")

with st.form("kyc_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    country = st.selectbox("Country", ["United States","Brazil","Mexico","Colombia","Argentina",
                                       "Vietnam","Zimbabwe","South Africa","Lebanon","Jordan","India","Bangladesh","Other"])
    id_uploaded = st.file_uploader("Upload ID image (simulated)", type=["png","jpg","jpeg"])
    approved = st.checkbox("Simulate KYC as PASSED")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if approved and name and email:
            st.success("✅ KYC Passed. You can proceed to link accounts.")
            st.session_state["kyc"] = {"name": name, "email": email, "country": country, "status": "passed", "ts": str(datetime.utcnow())}
        else:
            st.error("Please provide name, email, and mark KYC as PASSED for the demo.")