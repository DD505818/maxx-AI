"""Run accelerated trading simulation."""

from __future__ import annotations

import argparse
import asyncio
from typing import Any, Dict

from backend.services.trading_engine import TradingEngine


async def run_sim(hours: float, starting_balance: float) -> Dict[str, Any]:
    """Run engine for specified hours and return final stats."""
    engine = TradingEngine(starting_balance=starting_balance, tick_delay=0.0, order_delay=0.0)
    ticks = int(hours * 3600 / 0.5)
    await engine.start(ticks=ticks, ignore_session=True)
    return {
        "start_balance": starting_balance,
        "end_balance": engine.risk.balance,
        "unrealized_pnl": engine.risk.unrealized_pnl(),
        "total_fills": len(engine.risk.fills),
    }


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=float, default=72.0)
    parser.add_argument("--balances", type=float, nargs="*", default=[100, 1000, 2000])
    args = parser.parse_args()

    for bal in args.balances:
        res = await run_sim(args.hours, bal)
        print(res)


if __name__ == "__main__":
    asyncio.run(main())
