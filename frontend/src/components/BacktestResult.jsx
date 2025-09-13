function BacktestResult({ result }) {
  return (
    <div className="border p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Simulation Result</h2>
      <p><strong>Profit/Loss:</strong> ${result.pnl}</p>
      <p><strong>Orders Executed:</strong> {result.orders}</p>
      <p><strong>Status:</strong> {result.success ? "Success" : "Failed"}</p>
    </div>
  );
}

export default BacktestResult;
