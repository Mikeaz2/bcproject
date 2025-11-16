import streamlit as st
import pandas as pd
from utils.scoring import compute_features, rule_based_score

st.set_page_config(page_title="Lender Portal – BC", page_icon="🏦", layout="wide")
st.title("Lender Portal (Demo)")

tx = st.session_state.get("transactions", pd.DataFrame(columns=["date","amount","type","category"]))
feats = compute_features(tx)
score, band = rule_based_score(feats)

st.subheader("Borrower Snapshot")
st.write({"Score": score, "Band": band, **feats})

st.subheader("Risk Tier Pools (Illustrative)")
st.table(pd.DataFrame([
    {"Tier":"Prime","Band":"86–100","Expected Loss":"Low","Target APY":"6–8%","Pool Size":"$250k"},
    {"Tier":"Green","Band":"70–85","Expected Loss":"Low–Med","Target APY":"8–10%","Pool Size":"$150k"},
    {"Tier":"Amber","Band":"50–69","Expected Loss":"Med","Target APY":"12–15%","Pool Size":"$100k"},
    {"Tier":"Red","Band":"0–49","Expected Loss":"High","Target APY":"18–24%","Pool Size":"$50k"},
]))