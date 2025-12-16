import asyncio
import json
import websockets
from datetime import datetime
from backend.database import SessionLocal, Tick
from backend.resampler import add_tick

BINANCE_WS_URL = "wss://stream.binance.com:9443/stream"
SYMBOLS = ["btcusdt", "ethusdt"]


def build_stream_url():
    streams = "/".join([f"{s}@trade" for s in SYMBOLS])
    return f"{BINANCE_WS_URL}?streams={streams}"


async def consume_trades():
    url = build_stream_url()

    while True:
        try:
            async with websockets.connect(url) as ws:
                print("✅ Connected to Binance WebSocket")

                async for message in ws:
                    payload = json.loads(message)
                    trade = payload["data"]

                    symbol = trade["s"]
                    price = float(trade["p"])
                    qty = float(trade["q"])
                    timestamp = datetime.fromtimestamp(trade["T"] / 1000)

                    tick = Tick(
                        symbol=symbol,
                        price=price,
                        quantity=qty,
                        timestamp=timestamp
                    )

                    db = SessionLocal()
                    db.add(tick)
                    db.commit()
                    db.close()

                    # Push to in-memory buffer
                    add_tick(symbol, price, qty, timestamp)

        except Exception as e:
            print("❌ WebSocket error:", e)
            await asyncio.sleep(2)
