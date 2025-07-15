"""FastAPI entrypoint for MAXX-AI backend."""

from __future__ import annotations

import asyncio
import logging
from typing import AsyncGenerator

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from ..services.trading_engine import TradingEngine
from ..models.agent_state import AgentState

app = FastAPI(title="MAXX-AI")
engine = TradingEngine()
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(engine.start())


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.websocket("/ws/agents")
async def agents_ws(ws: WebSocket) -> None:
    await ws.accept()
    try:
        async for state in engine.state_stream():
            data = AgentState(**state)
            await ws.send_json(data.__dict__)
    except WebSocketDisconnect:
        logger.info("client disconnected")
