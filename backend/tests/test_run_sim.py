from backend.pipelines.run_sim import run_sim
import asyncio


def test_run_sim_returns_dict() -> None:
    res = asyncio.run(run_sim(0.001, 100.0))
    assert "end_balance" in res

