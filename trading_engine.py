import asyncio, os, time, logging
from .market_data import TickSubscriber
from .session_clock import session_active
from .sentiment_bridge import sentiment_factor
from .alpha_ensemble import AlphaEngine
from .order_router import Router
from .risk_manager import RiskSentinel
from ..models.plan_v2 import PlanV2, Leg

logger = logging.getLogger("MAXXAI_ENGINE")

class TradingEngine:
    def __init__(self):
        self.tick_sub = TickSubscriber(["BTCUSD","ETHUSD","EURUSD"])
        self.alpha    = AlphaEngine()
        self.router   = Router()
        self.risk     = RiskSentinel()
        self.ws_queues = []

    async def state_stream(self):
        q = asyncio.Queue()
        self.ws_queues.append(q)
        try:
            while True:
                yield await q.get()
        finally:
            self.ws_queues.remove(q)

    async def _broadcast(self, state):
        for q in self.ws_queues:
            await q.put(state)

    async def start(self):
        async for tick in self.tick_sub.stream():
            if not session_active():
                continue
            sent = await sentiment_factor()
            alpha = self.alpha.score(tick.symbol)*(1+0.5*sent)
            if abs(alpha) < .25 or self.risk.halt:
                continue
            qty = self.alpha.size(tick.price, self.risk.balance, alpha)
            plan = PlanV2(timestamp=time.time(),
                          legs=[Leg(symbol=tick.symbol,
                                    side="BUY" if alpha>0 else "SELL",
                                    qty=qty,
                                    broker=self.router.best_venue(tick.symbol))])
            fill = await self.router.execute(plan.legs[0])
            self.risk.update(fill)
            await self._broadcast({"symbol":tick.symbol,"balance":self.risk.balance})
