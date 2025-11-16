import streamlit as st
import pandas as pd
from utils.data import sample_transactions_bank, sample_transactions_mobile_money, normalize_columns

st.set_page_config(page_title="Link Accounts – BC", page_icon="🏦", layout="wide")
st.title("Link Accounts (Sandbox / CSV)")

st.markdown("Choose a source below. For the demo, you can generate **sample transactions** or **upload CSV**.")

tab1, tab2, tab3 = st.tabs(["Bank (Plaid-like Sandbox)","Mobile Money (EcoCash/M-Pesa/MoMo/ZaloPay)","Upload CSV"])

if "transactions" not in st.session_state:
    st.session_state["transactions"] = pd.DataFrame(columns=["date","amount","type","category"])

with tab1:
    st.write("Simulate bank transactions (salary + typical spend)")
    if st.button("Generate Bank Sample"):
        df = sample_transactions_bank()
        st.session_state["transactions"] = pd.concat([st.session_state["transactions"], df], ignore_index=True)
        st.success(f"Added {len(df)} bank transactions.")
        st.dataframe(df)

with tab2:
    st.write("Simulate mobile money flows (EcoCash / M-Pesa / MoMo / ZaloPay)")
    if st.button("Generate Mobile-Money Sample"):
        df = sample_transactions_mobile_money()
        st.session_state["transactions"] = pd.concat([st.session_state["transactions"], df], ignore_index=True)
        st.success(f"Added {len(df)} mobile-money transactions.")
        st.dataframe(df)

with tab3:
    up = st.file_uploader("Upload CSV with columns: date, amount, type (inflow/outflow), category", type=["csv"])
    if up is not None:
        df = pd.read_csv(up)
        df = normalize_columns(df)
        st.session_state["transactions"] = pd.concat([st.session_state["transactions"], df], ignore_index=True)
        st.success(f"Uploaded {len(df)} transactions from CSV.")
        st.dataframe(df.head())

st.divider()
if not st.session_state["transactions"].empty:
    st.subheader("All Linked Transactions")
    st.dataframe(st.session_state["transactions"])
else:
    st.info("No transactions linked yet.")