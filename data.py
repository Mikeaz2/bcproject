import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def sample_transactions_bank():
    # simple synthetic bank transactions for 6 months
    rows = []
    today = datetime.today().date().replace(day=1)
    for m in range(6):
        month_start = (today - pd.DateOffset(months=m)).to_timestamp()
        # inflow: salary or freelance
        rows.append({"date": month_start + pd.Timedelta(days=1), "amount": 900.00, "type": "inflow", "category": "salary"})
        # outflows
        rows.append({"date": month_start + pd.Timedelta(days=3), "amount": 450.00, "type": "outflow", "category": "rent"})
        rows.append({"date": month_start + pd.Timedelta(days=10), "amount": 120.00, "type": "outflow", "category": "groceries"})
        rows.append({"date": month_start + pd.Timedelta(days=18), "amount": 60.00, "type": "outflow", "category": "transport"})
    return pd.DataFrame(rows)

def sample_transactions_mobile_money():
    rows = []
    today = datetime.today().date().replace(day=1)
    for m in range(6):
        month_start = (today - pd.DateOffset(months=m)).to_timestamp()
        rows.append({"date": month_start + pd.Timedelta(days=2), "amount": 300.00, "type": "inflow", "category": "ecocash_gig"})
        rows.append({"date": month_start + pd.Timedelta(days=4), "amount": 200.00, "type": "outflow", "category": "wallet_spend"})
        rows.append({"date": month_start + pd.Timedelta(days=14), "amount": 50.00, "type": "inflow", "category": "remittance_in"})
    return pd.DataFrame(rows)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure expected columns exist
    expected = ["date","amount","type","category"]
    for col in expected:
        if col not in df.columns:
            df[col] = None
    df = df[expected].copy()
    return df