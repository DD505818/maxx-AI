"""Channel breakout strategy for crypto."""
from __future__ import annotations

import pandas as pd
from typing import Tuple


class CryptoChannelBreakout:
    """Breakout when price leaves recent channel."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        if len(data) < 30:
            return None, 0.0
        high = data.high.rolling(window=20).max()
        low = data.low.rolling(window=20).min()
        if data.close.iloc[-1] > high.iloc[-2]:
            return "buy", 0.6
        if data.close.iloc[-1] < low.iloc[-2]:
            return "sell", 0.6
        return None, 0.0
