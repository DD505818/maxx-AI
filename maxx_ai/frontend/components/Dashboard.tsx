import { useEffect, useState } from "react";
import BacktestPanel from "./BacktestPanel";

interface Metrics {
  pnl: number;
  trades: number;
  win_rate: number;
}

const Dashboard = () => {
  const [metrics, setMetrics] = useState<Metrics>({ pnl: 0, trades: 0, win_rate: 0 });
  const [tradeLog, setTradeLog] = useState<any[]>([]);
  const [equityHistory, setEquityHistory] = useState<number[]>([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = (ev) => {
      const data = JSON.parse(ev.data);
      setMetrics(data.metrics);
      setTradeLog(data.trade_log);
      setEquityHistory(data.equity_history);
    };
    return () => ws.close();
  }, []);

  return (
    <div>
      <h1>MAXX AI Dashboard</h1>
      <p>PnL: {metrics.pnl.toFixed(2)}</p>
      <p>Trades: {metrics.trades}</p>
      <p>Win Rate: {(metrics.win_rate * 100).toFixed(1)}%</p>
      <BacktestPanel />
    </div>
  );
};

export default Dashboard;
