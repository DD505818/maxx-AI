"""Run an accelerated trading simulation from the command line."""

from __future__ import annotations

import argparse
import asyncio
from typing import Tuple

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from backend.services.market_data import TickSubscriber
from backend.services.risk_manager import RiskSentinel
from backend.services.trading_engine import TradingEngine


async def simulate(initial_balance: float, hours: int = 72) -> Tuple[float, int]:
    """Run the engine for ``hours`` trading hours and return final balance.

    The simulation runs without tick delays to complete quickly.
    Each hour is approximated by one tick.
    """

    ticks = int(hours)
    sub = TickSubscriber(["BTCUSD", "ETHUSD", "EURUSD"], delay=0.0)
    engine = TradingEngine(tick_sub=sub, risk=RiskSentinel(start_balance=initial_balance))
    await engine.run(ticks)
    return engine.risk.balance, ticks


def main() -> None:
    parser = argparse.ArgumentParser(description="Run trading simulation")
    parser.add_argument("initial", type=float, help="initial balance")
    parser.add_argument("--hours", type=int, default=72, help="simulation hours")
    args = parser.parse_args()
    final_balance, ticks = asyncio.run(simulate(args.initial, args.hours))
    print(f"start={args.initial} final={final_balance:.2f} ticks={ticks}")


if __name__ == "__main__":
    main()
