import pandas as pd
from fastapi import APIRouter
from backend.database import SessionLocal
from backend.analytics.hedge_ratio import ols_hedge_ratio
from backend.analytics.kalman import kalman_hedge_ratio
from backend.analytics.spread import compute_spread
from backend.analytics.zscore import zscore
from backend.analytics.correlation import rolling_correlation
from backend.analytics.backtest import mean_reversion_backtest

router = APIRouter()


@router.get("/analytics/pair")
def pair_analytics(
    symbol_a: str = "BTCUSDT",
    symbol_b: str = "ETHUSDT",
    timeframe: str = "1m",
    window: int = 100,
    entry_z: float = 2.0
):
    db = SessionLocal()

    a = pd.read_sql(
        f"""
        SELECT timestamp, close FROM resampled_bars
        WHERE symbol='{symbol_a}' AND timeframe='{timeframe}'
        ORDER BY timestamp
        """,
        db.bind
    )

    b = pd.read_sql(
        f"""
        SELECT timestamp, close FROM resampled_bars
        WHERE symbol='{symbol_b}' AND timeframe='{timeframe}'
        ORDER BY timestamp
        """,
        db.bind
    )

    db.close()

    if len(a) < window or len(b) < window:
        return {"error": "Not enough data"}

    merged = a.merge(b, on="timestamp", suffixes=("_a", "_b"))

    # Hedge ratios
    ols_beta = ols_hedge_ratio(
        merged["close_a"], merged["close_b"]
    )

    kalman_beta = kalman_hedge_ratio(
        merged["close_a"], merged["close_b"]
    )

    # Spread (Kalman hedge)
    merged["spread"] = compute_spread(
        merged["close_a"], merged["close_b"], kalman_beta
    )

    # Z-score series
    merged["z"] = (
        merged["spread"]
        .rolling(window)
        .apply(lambda x: (x.iloc[-1] - x.mean()) / x.std() if x.std() != 0 else 0)
    )

    backtest = mean_reversion_backtest(
        merged["spread"], merged["z"], entry_threshold=entry_z
    )

    return {
        "ols_hedge_ratio": ols_beta,
        "kalman_hedge_ratio": kalman_beta,
        "latest_z_score": float(merged["z"].iloc[-1]),
        "rolling_correlation": rolling_correlation(
            merged["close_a"], merged["close_b"], window
        ),
        "backtest": backtest
    }
