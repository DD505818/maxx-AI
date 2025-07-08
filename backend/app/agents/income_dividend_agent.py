"""
IncomeDividendAgent — AI agent implementing a dividend‑focused, low‑volatility, compounding strategy.
Follows 'Millionaire Next Door Dividend Investor’s Playbook'.
"""

class IncomeDividendAgent:
    def __init__(self, capital, universe):
        self.capital = capital
        self.universe = universe
        self.portfolio = {}

    def evaluate(self):
        ranked = sorted(self.universe, key=lambda x: (x.dividend_yield, -x.volatility), reverse=True)
        self.portfolio = {s.symbol: self.capital / len(ranked) for s in ranked[:5]}
        return self.portfolio

    def rebalance(self, market_data):
        self.evaluate()
        print(f"Rebalanced portfolio: {self.portfolio}")
