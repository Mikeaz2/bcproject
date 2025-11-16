import numpy as np
import pandas as pd

def compute_features(transactions: pd.DataFrame) -> dict:
    # Expect columns: date, amount, type ('inflow'/'outflow'), category
    df = transactions.copy()
    if df.empty:
        return {
            "avg_inflow": 0.0,
            "income_volatility": 1.0,
            "expense_ratio": 1.0,
            "overdraft_count": 0,
            "remittance_count": 0,
            "gig_months_active": 0,
            "mobile_money_signal": False,
        }

    # Ensure correct types
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["type"] = df["type"].str.lower()

    # Monthly inflow / outflow
    df["ym"] = df["date"].dt.to_period("M")
    inflows = df[df["type"]=="inflow"].groupby("ym")["amount"].sum().astype(float)
    outflows = df[df["type"]=="outflow"].groupby("ym")["amount"].sum().astype(float)

    avg_inflow = float(inflows.mean()) if len(inflows) else 0.0
    income_volatility = float(inflows.std() / inflows.mean()) if len(inflows) and inflows.mean()!=0 else 1.0
    total_in = float(df.loc[df["type"]=="inflow","amount"].sum())
    total_out = float(df.loc[df["type"]=="outflow","amount"].sum())
    expense_ratio = float(total_out / total_in) if total_in>0 else 1.0

    # Simple overdraft proxy: months where outflow > inflow by 10%
    overdraft_count = int(sum((outflows.reindex(inflows.index, fill_value=0) > inflows * 1.1)))

    # Alternative signals
    categories = (df.get("category") or pd.Series(dtype=str)).astype(str).str.lower()
    remittance_count = int(((categories.str.contains("remittance")) | (categories.str.contains("transfer_international"))).sum())
    gig_months_active = int((df[df["category"].str.lower().str.contains("gig|upwork|fiverr|delivery|rappi|grab", na=False)]
                             .groupby("ym")["amount"].sum().shape[0]))

    # Mobile money signal: if source contains ecocash/mpesa/momo/zalopay in categories or any wallet hint
    mobile_money_signal = bool(categories.str.contains("ecocash|mpesa|m-pesa|momo|zalopay|wallet", regex=True).any())

    return {
        "avg_inflow": round(avg_inflow,2),
        "income_volatility": round(float(income_volatility),2),
        "expense_ratio": round(float(expense_ratio),2),
        "overdraft_count": int(overdraft_count),
        "remittance_count": int(remittance_count),
        "gig_months_active": int(gig_months_active),
        "mobile_money_signal": mobile_money_signal,
    }

def rule_based_score(feats: dict) -> tuple[int, str]:
    score = 50

    # avg_inflow
    if feats["avg_inflow"] >= 800:
        score += 15
    elif feats["avg_inflow"] >= 400:
        score += 5

    # income volatility
    if feats["income_volatility"] > 0.6:
        score -= 10
    elif feats["income_volatility"] > 0.4:
        score -= 5

    # expense ratio
    if feats["expense_ratio"] > 0.95:
        score -= 12
    elif feats["expense_ratio"] > 0.8:
        score -= 6
    elif feats["expense_ratio"] < 0.6:
        score += 4

    # overdrafts
    score -= min(24, 8 * feats["overdraft_count"])

    # remittances
    if feats["remittance_count"] >= 3:
        score += 6

    # gig activity
    if feats["gig_months_active"] >= 3:
        score += 8

    # mobile money
    if feats["mobile_money_signal"]:
        score += 4

    score = max(0, min(100, score))

    if score >= 86:
        band = "Prime"
    elif score >= 70:
        band = "Green"
    elif score >= 50:
        band = "Amber"
    else:
        band = "Red"

    return int(score), band