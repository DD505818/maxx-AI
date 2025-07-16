interface MetricsProps {
  metrics: { pnl: number; trades: number; win_rate: number };
}

const MetricsDisplay = ({ metrics }: MetricsProps) => (
  <ul>
    <li>PnL: {metrics.pnl.toFixed(2)}</li>
    <li>Trades: {metrics.trades}</li>
    <li>Win Rate: {(metrics.win_rate * 100).toFixed(1)}%</li>
  </ul>
);

export default MetricsDisplay;
