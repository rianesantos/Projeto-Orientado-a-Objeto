from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from ..services.market_service import fetch_intraday_ohlcv, fetch_latest_quote
from ..services.indicators import sma, rsi
import asyncio
import pandas as pd
import json

router = APIRouter(prefix="/market-data", tags=["Market Data"])

@router.get("/quote/{symbol}")
def get_quote(symbol: str):
    q = fetch_latest_quote(symbol)
    if q is None:
        raise HTTPException(status_code=404, detail="Symbol not found or no data")
    return q

@router.get("/ohlcv/{symbol}")
def get_ohlcv(symbol: str, period: str = "7d", interval: str = "1h"):
    df = fetch_intraday_ohlcv(symbol, period=period, interval=interval)
    if df.empty:
        raise HTTPException(status_code=404, detail="No OHLCV data")
    # return JSON serializable: list of dicts
    payload = []
    for idx, row in df.iterrows():
        payload.append({
            "datetime": idx.isoformat(),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"])
        })
    return {"symbol": symbol, "series": payload}

@router.get("/indicators/{symbol}")
def get_indicators(symbol: str, period: str = "30d", interval: str = "1d", sma_window: int = 20, rsi_window: int = 14):
    df = fetch_intraday_ohlcv(symbol, period=period, interval=interval)
    if df.empty:
        raise HTTPException(status_code=404, detail="No data for indicators")
    closes = df["Close"]
    sma_series = sma(closes, sma_window).dropna()
    rsi_series = rsi(closes, rsi_window).dropna()
    # return latest indicator values
    return {
        "symbol": symbol,
        "latest_close": float(closes.iloc[-1]),
        "sma": float(sma_series.iloc[-1]) if not sma_series.empty else None,
        "rsi": float(rsi_series.iloc[-1]) if not rsi_series.empty else None
    }

# Simple websocket that sends the latest quote periodically
@router.websocket("/ws/{symbol}")
async def websocket_market(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            q = fetch_latest_quote(symbol)
            if q:
                await websocket.send_text(json.dumps(q))
            await asyncio.sleep(5)  # frequency: 5s (adjust)
    except WebSocketDisconnect:
        return
    except Exception:
        await websocket.close()