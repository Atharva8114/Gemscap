import asyncio
from fastapi import FastAPI
from backend.database import init_db
from backend.websocket_client import consume_trades
from backend.resampler import resample_ticks
from backend.api import router

SYMBOLS = ["BTCUSDT", "ETHUSDT"]
TIMEFRAMES = ["1s", "1m", "5m"]

app = FastAPI(title="Quant Analytics Backend")
app.include_router(router)


async def resampling_loop():
    while True:
        for symbol in SYMBOLS:
            for tf in TIMEFRAMES:
                resample_ticks(symbol, tf)
        await asyncio.sleep(1)


@app.on_event("startup")
async def startup_event():
    init_db()
    asyncio.create_task(consume_trades())
    asyncio.create_task(resampling_loop())
    print("🚀 Backend started (Ingestion + Resampling + Analytics)")


@app.get("/")
def health():
    return {"status": "running"}
