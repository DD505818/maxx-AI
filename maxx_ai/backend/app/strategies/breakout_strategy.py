"""Generic breakout strategy."""
from __future__ import annotations

import pandas as pd
from typing import Tuple


class BreakoutStrategy:
    """Enter on new highs or lows over last 50 bars."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        if len(data) < 50:
            return None, 0.0
        high = data.high.rolling(window=50).max()
        low = data.low.rolling(window=50).min()
        if data.close.iloc[-1] > high.iloc[-2]:
            return "buy", 0.5
        if data.close.iloc[-1] < low.iloc[-2]:
            return "sell", 0.5
        return None, 0.0
