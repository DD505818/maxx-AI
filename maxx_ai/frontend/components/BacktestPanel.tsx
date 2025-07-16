import React, { useState } from "react";

const BacktestPanel = () => {
  const [file, setFile] = useState<File | null>(null);
  const [strategy, setStrategy] = useState<string>("triple_ma");
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const strategies = [
    { label: "Triple MA", value: "triple_ma" },
    { label: "Stochastic", value: "stochastic" },
    { label: "Ichimoku", value: "ichimoku" },
    { label: "Channel Breakout", value: "channel" },
    { label: "MACD Histogram", value: "macd_histogram" },
    { label: "Bollinger Squeeze", value: "bollinger_squeeze" },
    { label: "Momentum", value: "momentum" },
    { label: "Mean Reversion", value: "mean_reversion" },
    { label: "Breakout", value: "breakout" },
    { label: "ORB", value: "orb" },
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) setFile(e.target.files[0]);
  };

  const handleBacktest = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("strategy", strategy);

    const res = await fetch("/api/backtest", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setResults(data);
    setLoading(false);
  };

  return (
    <div className="backtest-panel">
      <h2>Strategy Backtest</h2>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <select value={strategy} onChange={(e) => setStrategy(e.target.value)}>
        {strategies.map((s) => (
          <option value={s.value} key={s.value}>
            {s.label}
          </option>
        ))}
      </select>
      <button onClick={handleBacktest} disabled={loading}>
        {loading ? "Running..." : "Run Backtest"}
      </button>
      {results && (
        <div>
          <h3>Equity Curve</h3>
          <pre style={{ maxHeight: 150, overflow: "auto", background: "#f6f8fa" }}>
            {JSON.stringify(results.equity_curve, null, 2)}
          </pre>
          <h3>Trades</h3>
          <pre style={{ maxHeight: 150, overflow: "auto", background: "#f6f8fa" }}>
            {JSON.stringify(results.trades, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default BacktestPanel;
