interface Trade {
  timestamp: string;
  symbol: string;
  side: string;
  price: number;
  size: number;
}

const TradeLog = ({ trades }: { trades: Trade[] }) => (
  <table>
    <thead>
      <tr>
        <th>Time</th>
        <th>Symbol</th>
        <th>Side</th>
        <th>Price</th>
        <th>Size</th>
      </tr>
    </thead>
    <tbody>
      {trades.map((t, i) => (
        <tr key={i}>
          <td>{t.timestamp}</td>
          <td>{t.symbol}</td>
          <td>{t.side}</td>
          <td>{t.price}</td>
          <td>{t.size}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default TradeLog;
