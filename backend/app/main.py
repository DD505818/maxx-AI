from collections import namedtuple
from fastapi import FastAPI
from .agents.income_dividend_agent import IncomeDividendAgent

app = FastAPI()

@app.get("/portfolio")
def read_portfolio():
    Stock = namedtuple("Stock", ["symbol", "dividend_yield", "volatility"])
    universe = [
        Stock("AAA", 0.05, 0.2),
        Stock("BBB", 0.04, 0.1),
        Stock("CCC", 0.06, 0.3),
    ]
    agent = IncomeDividendAgent(capital=10000, universe=universe)
    portfolio = agent.evaluate()
    return portfolio
