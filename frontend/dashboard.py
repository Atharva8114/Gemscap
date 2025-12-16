import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Pairs Trading Dashboard", layout="wide")

st.title("📊 Crypto Pairs Trading Dashboard")

# =====================
# Sidebar Controls
# =====================
st.sidebar.header("Configuration")

symbol_a = st.sidebar.selectbox("Symbol A", ["BTCUSDT", "ETHUSDT"], index=0)
symbol_b = st.sidebar.selectbox("Symbol B", ["ETHUSDT", "BTCUSDT"], index=1)

timeframe = st.sidebar.selectbox("Timeframe", ["1s", "1m", "5m"], index=1)
window = st.sidebar.slider("Rolling Window", 10, 200, 50)
entry_z = st.sidebar.slider("Entry Z-Score", 1.0, 3.0, 2.0)

refresh = st.sidebar.button("🔄 Refresh Analytics")

# =====================
# Fetch Data
# =====================
params = {
    "symbol_a": symbol_a,
    "symbol_b": symbol_b,
    "timeframe": timeframe,
    "window": window,
    "entry_z": entry_z
}

response = requests.get(f"{API_URL}/analytics/pair", params=params)

if response.status_code != 200:
    st.error("Backend not reachable")
    st.stop()

data = response.json()

if "error" in data:
    st.warning(data["error"])
    st.stop()

# =====================
# Metrics
# =====================
col1, col2, col3, col4 = st.columns(4)

col1.metric("OLS Hedge Ratio", round(data["ols_hedge_ratio"], 3))
col2.metric("Kalman Hedge Ratio", round(data["kalman_hedge_ratio"], 3))
col3.metric("Latest Z-Score", round(data["latest_z_score"], 3))
col4.metric("Rolling Correlation", round(data["rolling_correlation"], 3))

# =====================
# Z-Score Alert
# =====================
if abs(data["latest_z_score"]) >= entry_z:
    st.error(
        f"🚨 Z-Score Alert! |Z| ≥ {entry_z} (Current: {round(data['latest_z_score'], 2)})"
    )

# =====================
# Backtest Results
# =====================
st.subheader("📈 Mini Backtest Summary")

bt = data["backtest"]

bt_col1, bt_col2, bt_col3, bt_col4 = st.columns(4)

bt_col1.metric("Total Trades", bt["total_trades"])
bt_col2.metric("Total PnL", round(bt["total_pnl"], 2))
bt_col3.metric("Avg PnL", round(bt["avg_pnl"], 2))
bt_col4.metric("Max Drawdown", round(bt["max_drawdown"], 2))

# =====================
# PnL Distribution
# =====================
if bt["pnl_series"]:
    pnl_df = pd.DataFrame(bt["pnl_series"], columns=["PnL"])
    st.bar_chart(pnl_df)

# =====================
# Export CSV
# =====================
st.subheader("⬇️ Export Backtest PnL")

if bt["pnl_series"]:
    csv = pnl_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        file_name="backtest_pnl.csv",
        mime="text/csv",
    )
else:
    st.info("No trades yet to export.")
