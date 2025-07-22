"""Portfolio analytics utilities."""
from __future__ import annotations

import pandas as pd


class AnalyticsService:
    """Compute metrics and maintain trade log."""

    def __init__(self) -> None:
        self._trade_log = pd.DataFrame(
            columns=["timestamp", "symbol", "side", "price", "size", "profit"]
        )

    def get_trade_log(self) -> pd.DataFrame:
        return self._trade_log

    def record_trade(self, trade: dict) -> None:
        self._trade_log = pd.concat(
            [self._trade_log, pd.DataFrame([trade])], ignore_index=True
        )

    def get_metrics(self, portfolio: dict) -> dict:
        pnl = portfolio["equity_history"][-1] - portfolio["equity_history"][0]
        trades = len(self._trade_log)
        win_rate = (
            self._trade_log[self._trade_log.profit > 0].shape[0] / trades
            if trades
            else 0
        )
        return {"pnl": pnl, "trades": trades, "win_rate": win_rate}
