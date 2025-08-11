"""MACD histogram strategy."""
from __future__ import annotations

import pandas as pd
from typing import Tuple


class MACDHistogram:
    """Trade based on MACD histogram crossing zero."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        if len(data) < 35:
            return None, 0.0
        import pandas_ta as ta
        macd = ta.macd(data.close)
        hist = macd["MACDh_12_26_9"]
        if hist.iloc[-2] <= 0 and hist.iloc[-1] > 0:
            return "buy", 0.7
        if hist.iloc[-2] >= 0 and hist.iloc[-1] < 0:
            return "sell", 0.7
        return None, 0.0
