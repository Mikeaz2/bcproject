import streamlit as st

st.set_page_config(page_title="BC – Borderless Credit", page_icon="🌍", layout="wide")

st.title("BC – Borderless Credit")
st.subheader("Build Credit Without Borders")

st.markdown(
    '''
    **Prototype Goals**
    1. Onboard user (KYC – simulated) and link accounts (bank / mobile money / CSV)
    2. Compute a **portable credit score** from open-banking + alternative data
    3. Show instant **micro-loan offers**
    4. Provide a transparent **lender portal** view
    '''
)

st.info("Use the left sidebar to navigate through the demo pages.")