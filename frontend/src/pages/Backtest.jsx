import { useState } from "react";
import PageWrapper from "../components/PageWrapper";
import BacktestResult from "../components/BacktestResult";
import LoadingSpinner from "../components/LoadingSpinner";

function Backtest() {
  const [form, setForm] = useState({
    asset: "",
    condition: "",
    rule: "",
    start: "",
    end: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!form.asset || !form.condition || !form.rule || !form.start || !form.end) {
      alert("Preencha todos os campos.");
      return;
    }

    if (form.start > form.end) {
      alert("A data inicial deve ser anterior à final.");
      return;
    }

    setLoading(true);

    setTimeout(() => {
      setResult({
        pnl: 1250.75,
        orders: 14,
        success: true,
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <PageWrapper>
      <h1 className="text-3xl font-bold text-white mb-6">Backtest Simulator</h1>

      <form
        onSubmit={handleSubmit}
        className="space-y-6 bg-gray-900 p-6 rounded-xl shadow-lg border border-gray-700"
      >
        <div>
          <label className="block text-sm font-medium text-purple-300 mb-1">Asset</label>
          <input
            type="text"
            name="asset"
            value={form.asset}
            onChange={handleChange}
            className="w-full bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
            placeholder="e.g. PETR4"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-purple-300 mb-1">Condition</label>
          <input
            type="text"
            name="condition"
            value={form.condition}
            onChange={handleChange}
            className="w-full bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
            placeholder="e.g. price > 20"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-purple-300 mb-1">Rule</label>
          <input
            type="text"
            name="rule"
            value={form.rule}
            onChange={handleChange}
            className="w-full bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
            placeholder="e.g. buy"
            required
          />
        </div>

        <div className="flex gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-purple-300 mb-1">Start Date</label>
            <input
              type="date"
              name="start"
              value={form.start}
              onChange={handleChange}
              className="w-full bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
              required
            />
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium text-purple-300 mb-1">End Date</label>
            <input
              type="date"
              name="end"
              value={form.end}
              onChange={handleChange}
              className="w-full bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
              required
            />
          </div>
        </div>

        <button
          type="submit"
          className="bg-purple-600 text-white px-6 py-2 rounded-md hover:bg-purple-700 hover:scale-105 transition-transform duration-200 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Simulating..." : "Simulate"}
        </button>
      </form>

      <div className="mt-6">
        {loading && <LoadingSpinner message="Running simulation..." />}
        {result && !loading && <BacktestResult result={result} />}
      </div>
    </PageWrapper>
  );
}

export default Backtest;
