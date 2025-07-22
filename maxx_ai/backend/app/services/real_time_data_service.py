"""Provide 15 minute price data for backtesting and live trading."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import List

import pandas as pd


class RealTimeDataService:
    """Generate or load OHLCV data for given symbols."""

    async def start_stream(self, symbols: List[str]) -> None:
        """Stub for starting a live data stream."""
        await asyncio.sleep(0)

    async def get_15min_data(self, symbol: str) -> pd.DataFrame:
        """Return synthetic 15 minute data for the last day."""
        end = datetime.utcnow()
        start = end - timedelta(hours=24)
        rng = pd.date_range(start, end, freq="15min")
        df = pd.DataFrame(index=rng)
        df["open"] = 100.0
        df["high"] = df["open"] + 1.0
        df["low"] = df["open"] - 1.0
        df["close"] = df["open"]
        df["volume"] = 1.0
        return df
