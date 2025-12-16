# Real-Time Crypto Pairs Trading Dashboard

## 📌 Overview
This project is an **end-to-end real-time crypto pairs trading analytics system** built to demonstrate quantitative finance concepts alongside backend and frontend engineering skills.

The system ingests **live market data** from Binance, resamples it into multiple timeframes, computes **statistical arbitrage signals**, runs a **mini mean-reversion backtest**, and visualizes everything through an interactive dashboard.

The project is intentionally designed to be **interview-ready**, focusing on clarity, correctness, and system design rather than over-optimization.

---

## 🧠 Key Features

- 📡 Live tick data ingestion via **Binance WebSocket**
- ⏱️ Multi-timeframe resampling (**1s, 1m, 5m**)
- 🗄️ Persistent storage using **SQLite**
- 📐 **OLS Hedge Ratio** (static relationship)
- 🔄 **Kalman Filter Hedge Ratio** (dynamic & adaptive)
- 📊 Spread & **Z-score** computation
- 🚨 Real-time **Z-score alerts**
- 📈 **Mini mean-reversion backtest**
- ⬇️ CSV export of backtest results
- 🖥️ Interactive **Streamlit dashboard**



---

## 🛠️ Technology Stack

| Layer | Technology |
|-----|-----------|
| Backend API | FastAPI |
| Real-Time Data | Binance WebSocket (Python) |
| Analytics | NumPy, Pandas, Statsmodels |
| State Estimation | Kalman Filter |
| Storage | SQLite + SQLAlchemy |
| Frontend | Streamlit |
| Language | Python 3.11 |

---

## 📈 Trading Logic (High Level)

### Hedge Ratio Estimation
- **OLS Regression** provides a static hedge ratio
- **Kalman Filter** dynamically adjusts the hedge ratio as market conditions change



### Signal Generation
- Z-score measures deviation of the spread from its rolling mean
- Mean-reversion assumption is used for trade signals

### Mini Backtest Logic
- **Entry**: |Z-score| > threshold
- **Exit**: Z-score reverts toward zero
- Strategy is intentionally simple to avoid overfitting

---

## 🔌 API Endpoint

### `GET /analytics/pair`

Returns analytics and backtest results for a selected symbol pair.

**Query Parameters**
- `symbol_a` (default: BTCUSDT)
- `symbol_b` (default: ETHUSDT)
- `timeframe` (1s, 1m, 5m)
- `window` (rolling window size)
- `entry_z` (z-score threshold)

---

## 🖥️ Frontend Dashboard

The Streamlit dashboard provides:
- Symbol & timeframe selection
- Rolling window and entry threshold controls
- Live analytics metrics
- Z-score alert popups
- Mini backtest performance summary
- CSV export of PnL data

---

## ▶️ How to Run Locally

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt





