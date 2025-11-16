import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.scoring import compute_features, rule_based_score

st.set_page_config(page_title="Credit Dashboard – BC", page_icon="📊", layout="wide")
st.title("AI Credit Dashboard")

tx = st.session_state.get("transactions", pd.DataFrame(columns=["date","amount","type","category"]))
feats = compute_features(tx)
score, band = rule_based_score(feats)

col1, col2 = st.columns([1,2], gap="large")

with col1:
    st.subheader("BC Score")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        number = {"suffix": " / 100"},
        gauge = {
            "axis": {"range": [0,100]},
            "bar": {"thickness": 0.3},
            "steps": [
                {"range":[0,50],"color":"#ffcccc"},
                {"range":[50,70],"color":"#ffe9b3"},
                {"range":[70,86],"color":"#ccf2d1"},
                {"range":[86,100],"color":"#b3e5ff"}
            ],
        },
        title = {"text": f"Band: {band}"}
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.metric("Avg Monthly Inflow", f"${feats['avg_inflow']}")
    st.metric("Income Volatility", feats["income_volatility"])
    st.metric("Expense Ratio", feats["expense_ratio"])

with col2:
    st.subheader("Drivers")
    st.write({
        "Overdraft Months": feats["overdraft_count"],
        "Remittance Count": feats["remittance_count"],
        "Gig Months Active": feats["gig_months_active"],
        "Mobile Money Signal": feats["mobile_money_signal"],
    })

    st.info("Tip: Reduce expense ratio, avoid overdrafts, and maintain consistent inflows to improve the score.")

if not tx.empty:
    st.divider()
    st.subheader("Recent Transactions")
    st.dataframe(tx.sort_values("date", ascending=False).head(20))