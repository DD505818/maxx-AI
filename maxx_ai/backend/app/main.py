"""FastAPI application exposing trading endpoints."""
from __future__ import annotations

import asyncio
import io
import logging
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import JSONResponse

from .services.broker_service import BrokerService
from .services.trading_service import TradingService
from .services.real_time_data_service import RealTimeDataService
from .services.stock_selection_service import StockSelectionService
from .services.analytics_service import AnalyticsService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("maxx-api")

app = FastAPI(title="MAXX AI Trading Platform")

broker_service = BrokerService()
data_service = RealTimeDataService()
stock_service = StockSelectionService()
trading_service = TradingService(broker_service, data_service, stock_service)
analytics_service = AnalyticsService()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        try:
            metrics = analytics_service.get_metrics(trading_service.portfolio)
            trade_log = analytics_service.get_trade_log().to_dict(orient="records")
            equity_history = trading_service.portfolio["equity_history"]
            await websocket.send_json(
                {
                    "metrics": metrics,
                    "trade_log": trade_log,
                    "equity_history": equity_history,
                }
            )
            await asyncio.sleep(5)
        except Exception as exc:  # pragma: no cover - connection closed
            logger.error("WebSocket error: %s", exc)
            break


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Starting MAXX AI trading platform...")
    asyncio.create_task(trading_service.main_loop())
    asyncio.create_task(data_service.start_stream(stock_service.select_stocks()))


@app.get("/health")
async def health_check() -> dict[str, Any]:
    await broker_service.check_health()
    return {"status": "healthy", "brokers": broker_service.health_status}


@app.post("/backtest")
async def backtest_api(
    file: UploadFile = File(...), strategy: str = "triple_ma"
) -> JSONResponse:
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content), parse_dates=True, index_col=0)
    strat_obj = trading_service.strategies.get(strategy)
    if not strat_obj:
        return JSONResponse(content={"error": "Invalid strategy"}, status_code=400)
    equity, trades = trading_service.run_backtest(df, strat_obj, strategy)
    return JSONResponse(content={"equity_curve": equity, "trades": trades})


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
