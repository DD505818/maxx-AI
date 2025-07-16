"""Open range breakout using first 30 minutes of trading."""
from __future__ import annotations

import asyncio
from typing import Tuple

import pandas as pd

from ..services.real_time_data_service import RealTimeDataService


class ORBStrategy:
    """Trade breakouts above or below the opening range."""

    def __init__(self, data_service: RealTimeDataService) -> None:
        self.data_service = data_service

    def generate_signal(self, symbol: str) -> Tuple[str | None, float]:
        data = asyncio.run(self.data_service.get_15min_data(symbol))
        first_two = data.iloc[:2]
        high = first_two.high.max()
        low = first_two.low.min()
        last_price = data.close.iloc[-1]
        if last_price > high:
            return "buy", 0.5
        if last_price < low:
            return "sell", 0.5
        return None, 0.0
