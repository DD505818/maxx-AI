"""MAXX-AI backend API."""

import asyncio
import logging
from fastapi import FastAPI, WebSocket

from ..services.trading_engine import TradingEngine

app = FastAPI()
engine = TradingEngine()
logger = logging.getLogger("MAXXAI_API")


@app.on_event("startup")
async def startup_event() -> None:
    asyncio.create_task(engine.start())


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}


@app.websocket("/ws/agents")
async def agent_stream(ws: WebSocket) -> None:
    await ws.accept()
    async for state in engine.state_stream():
        await ws.send_json(state)
