import streamlit as st
import pandas as pd
from utils.scoring import compute_features, rule_based_score

st.set_page_config(page_title="Micro-Loan – BC", page_icon="💸", layout="wide")
st.title("Instant Micro-Loan Offer")

tx = st.session_state.get("transactions", pd.DataFrame(columns=["date","amount","type","category"]))
feats = compute_features(tx)
score, band = rule_based_score(feats)

st.write(f"Your current band: **{band}** (Score {score})")

offer = None
if band == "Prime":
    offer = {"amount": 500, "apr": 12.0, "term": 6}
elif band == "Green":
    offer = {"amount": 300, "apr": 16.0, "term": 6}
elif band == "Amber":
    offer = {"amount": 150, "apr": 22.0, "term": 5}
else:
    offer = {"amount": 100, "apr": 28.0, "term": 4}

st.subheader("Your Offer")
st.write(f"Amount: ${offer['amount']}")
st.write(f"APR: {offer['apr']}%")
st.write(f"Term: {offer['term']} months")

if st.button("Accept Offer"):
    st.success("✅ Loan approved (demo). Funds will be available shortly.")