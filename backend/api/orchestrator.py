import os

import uvicorn
from fastapi import FastAPI

MODEL_URL = os.getenv("MODEL_ENDPOINT", "http://localhost:8000/v1")
cfg = [{"model": "llama3", "base_url": MODEL_URL}]


def get_chat() -> "GroupChat":
    """Instantiate and cache the group chat."""
    from autogen import Agent, GroupChat  # type: ignore

    if not hasattr(get_chat, "_chat"):
        market_scout = Agent("Scout", cfg, tools=["market_feed"])
        alpha_research = Agent("Researcher", cfg, tools=["backtest", "python"])
        risk_sentinel = Agent("Risk", cfg, tools=["risk_api"])
        governor = Agent("Governor", cfg, tools=["balance_api", "order_api"])
        get_chat._chat = GroupChat(  # type: ignore[attr-defined]
            agents=[market_scout, alpha_research, risk_sentinel, governor],
            messages=[
                {
                    "role": "system",
                    "content": "Goal: maximize Sharpe with ≤5% DD.",
                }
            ],
            max_turns=8,
        )
    return get_chat._chat  # type: ignore[attr-defined]


app = FastAPI()


@app.post("/orchestrate")
async def orchestrate() -> dict[str, str]:
    chat = get_chat()
    result = chat.run()
    return {"plan": result}


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}


def server_port() -> int:
    """Return service port from $PORT or default to 8080."""
    return int(os.getenv("PORT", "8080"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=server_port())
