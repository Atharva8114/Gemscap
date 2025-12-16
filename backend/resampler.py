from collections import defaultdict, deque
import pandas as pd
from backend.database import SessionLocal, ResampledBar

# ==============================
# Configuration
# ==============================

TICK_BUFFER_SIZE = 5000

# In-memory buffer: symbol -> deque of ticks
tick_buffer = defaultdict(lambda: deque(maxlen=TICK_BUFFER_SIZE))


# ==============================
# Public API
# ==============================

def add_tick(symbol: str, price: float, quantity: float, timestamp):
    """
    Called by the WebSocket consumer.
    Stores ticks in an in-memory buffer for low-latency analytics.
    """
    tick_buffer[symbol].append({
        "timestamp": timestamp,
        "price": price,
        "quantity": quantity
    })


def resample_ticks(symbol: str, timeframe: str):
    """
    Converts buffered ticks into OHLCV bars and persists
    ONLY the latest fully closed bar into SQLite.
    """

    if symbol not in tick_buffer or len(tick_buffer[symbol]) < 5:
        return

    # Convert buffer to DataFrame
    df = pd.DataFrame(list(tick_buffer[symbol]))
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)

    # Timeframe mapping (future-proof)
    rule_map = {
        "1s": "1s",
        "1m": "1min",
        "5m": "5min"
    }

    rule = rule_map.get(timeframe)
    if rule is None:
        return

    # Resample
    price_ohlc = df["price"].resample(
        rule, label="right", closed="right"
    ).ohlc()

    volume = df["quantity"].resample(
        rule, label="right", closed="right"
    ).sum()

    bars = price_ohlc.join(volume, how="inner")
    bars.columns = ["open", "high", "low", "close", "volume"]

    if bars.empty:
        return

    # Take ONLY the latest fully closed bar
    last_bar = bars.iloc[-1]
    ts = last_bar.name.to_pydatetime()

    db = SessionLocal()

    # Prevent duplicate inserts
    exists = db.query(ResampledBar).filter(
        ResampledBar.symbol == symbol,
        ResampledBar.timeframe == timeframe,
        ResampledBar.timestamp == ts
    ).first()

    if not exists:
        bar = ResampledBar(
            symbol=symbol,
            timeframe=timeframe,
            open=float(last_bar["open"]),
            high=float(last_bar["high"]),
            low=float(last_bar["low"]),
            close=float(last_bar["close"]),
            volume=float(last_bar["volume"]),
            timestamp=ts
        )
        db.add(bar)
        db.commit()

    db.close()
