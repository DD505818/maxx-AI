interface ChartProps {
  equity: number[];
}

const LiveChart = ({ equity }: ChartProps) => (
  <div>
    <h3>Equity History</h3>
    <pre style={{ maxHeight: 100, overflow: "auto", background: "#f6f8fa" }}>
      {JSON.stringify(equity, null, 2)}
    </pre>
  </div>
);

export default LiveChart;
