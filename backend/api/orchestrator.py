from fastapi import FastAPI
from autogen import Agent, GroupChat, config_list_from_json
import os, uvicorn

MODEL_URL = os.getenv("MODEL_ENDPOINT", "http://localhost:8000/v1")
cfg = [{"model": "llama3", "base_url": MODEL_URL}]

market_scout   = Agent("Scout", cfg, tools=["market_feed"])
alpha_research = Agent("Researcher", cfg, tools=["backtest", "python"])
risk_sentinel  = Agent("Risk", cfg, tools=["risk_api"])
governor       = Agent("Governor", cfg, tools=["balance_api", "order_api"])

chat = GroupChat(
    agents=[market_scout, alpha_research, risk_sentinel, governor],
    messages=[{"role":"system","content":"Goal: maximize Sharpe with ≤5% DD."}],
    max_turns=8,
)

app = FastAPI()

@app.post("/orchestrate")
async def orchestrate():
    result = chat.run()
    return {"plan": result}

@app.get("/healthz")
def healthz(): 
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
