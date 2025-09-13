function PortfolioTable({ data }) {
  return (
    <table className="w-full table-auto border-collapse">
      <thead>
        <tr className="bg-gray-100">
          <th className="border px-4 py-2 text-left">Asset</th>
          <th className="border px-4 py-2 text-left">Quantity</th>
          <th className="border px-4 py-2 text-left">Average Price</th>
          <th className="border px-4 py-2 text-left">Profit/Loss</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.asset}>
            <td className="border px-4 py-2">{item.asset}</td>
            <td className="border px-4 py-2">{item.quantity}</td>
            <td className="border px-4 py-2">${item.average_price}</td>
            <td className="border px-4 py-2">
              {item.pnl >= 0 ? (
                <span className="text-green-600">+${item.pnl}</span>
              ) : (
                <span className="text-red-600">-${Math.abs(item.pnl)}</span>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default PortfolioTable;
