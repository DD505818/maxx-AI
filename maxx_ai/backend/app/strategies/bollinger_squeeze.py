"""Bollinger squeeze strategy."""
from __future__ import annotations

import pandas as pd
from typing import Tuple


class BollingerSqueeze:
    """Buy when Bollinger band width expands after a squeeze."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        if len(data) < 30:
            return None, 0.0
        import pandas_ta as ta
        bb = ta.bbands(data.close)
        width = (bb["BBU_20_2.0"] - bb["BBL_20_2.0"]) / bb["BBM_20_2.0"]
        if width.iloc[-2] < width.quantile(0.1) and width.iloc[-1] > width.iloc[-2]:
            if data.close.iloc[-1] > bb["BBM_20_2.0"].iloc[-1]:
                return "buy", 0.6
            return "sell", 0.6
        return None, 0.0
