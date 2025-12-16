import pandas as pd
import numpy as np


def mean_reversion_backtest(
    spread: pd.Series,
    zscores: pd.Series,
    entry_threshold: float = 2.0
):
    """
    Simple mean-reversion backtest on spread using z-score.
    Returns trades, pnl series, and summary stats.
    """

    position = 0   # 1 = long spread, -1 = short spread
    entry_price = 0.0

    pnl = []
    trades = []

    for t in range(1, len(spread)):
        z = zscores.iloc[t]

        # Entry logic
        if position == 0:
            if z > entry_threshold:
                position = -1
                entry_price = spread.iloc[t]
                trades.append(("SHORT", spread.index[t], entry_price))

            elif z < -entry_threshold:
                position = 1
                entry_price = spread.iloc[t]
                trades.append(("LONG", spread.index[t], entry_price))

        # Exit logic
        elif position == 1 and z >= 0:
            pnl.append(spread.iloc[t] - entry_price)
            position = 0

        elif position == -1 and z <= 0:
            pnl.append(entry_price - spread.iloc[t])
            position = 0

    pnl_series = pd.Series(pnl)

    return {
        "total_trades": len(pnl),
        "total_pnl": float(pnl_series.sum()) if not pnl_series.empty else 0.0,
        "avg_pnl": float(pnl_series.mean()) if not pnl_series.empty else 0.0,
        "max_drawdown": float(pnl_series.min()) if not pnl_series.empty else 0.0,
        "pnl_series": pnl_series.tolist(),
        "trades": trades
    }
