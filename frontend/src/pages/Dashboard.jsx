import { useEffect, useState } from "react";
import api from "../services/api";
import PageWrapper from "../components/PageWrapper";
import LoadingSpinner from "../components/LoadingSpinner";
import {
  FiUser,
  FiTrendingUp,
  FiStar,
  FiAlertTriangle,
  FiPlayCircle,
  FiDollarSign,
} from "react-icons/fi";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale);

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [user, setUser] = useState(null);
  const [marketData, setMarketData] = useState(null);
  const [alert, setAlert] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [marketError, setMarketError] = useState(false);

  const fetchMarketData = async () => {
    try {
      const response = await api.get("/market-data/quote/IBM");
      setMarketData({
        price: response.data.price,
        volume: response.data.volume,
        symbol: response.data.symbol,
      });
      setAlert(null);
      setMarketError(false);
    } catch (err) {
      console.error("Error fetching market data:", err);
      setMarketError(true);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryRes, userRes] = await Promise.all([
          api.get("/analytics/user-summary"),
          api.get("/users/me"),
        ]);
        setSummary(summaryRes.data);
        setUser(userRes.data);
      } catch (err) {
        console.error("Error loading user data:", err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    fetchMarketData();

    const intervalId = setInterval(fetchMarketData, 5000);

    return () => clearInterval(intervalId);
  }, []);

  const chartData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [
      {
        label: "Volume",
        data: [1200, 1800, 1500, 2200, 2000, 2500],
        borderColor: "#7C3AED",
        backgroundColor: "rgba(124, 58, 237, 0.2)",
        tension: 0.4,
      },
    ],
  };

  if (loading) {
    return (
      <PageWrapper>
        <LoadingSpinner message="Loading data..." />
      </PageWrapper>
    );
  }

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white">
          Welcome, {user?.username || summary?.username || "User"} 👋
        </h1>
        <p className="text-purple-400 mt-2 text-lg">
          Here is a summary of your trading account
        </p>
        <p className="text-purple-300 mt-1">Email: {user?.email}</p>
      </div>

      {alert && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-800 p-4 rounded-lg mb-6 flex items-center gap-3 animate-pulse">
          <FiAlertTriangle className="text-xl" />
          <p>{alert}</p>
        </div>
      )}

      <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 p-4 rounded-lg mb-6 flex items-center gap-3 animate-pulse">
        <FiAlertTriangle className="text-xl" />
        <p>
          You have high-risk strategies. Review them before running new
          backtests.
        </p>
      </div>

      <div className="mb-6">
        <button className="flex items-center gap-2 bg-purple-600 text-white px-5 py-2 rounded-md hover:bg-purple-700 hover:scale-105 transition-transform">
          <FiPlayCircle className="text-lg" />
          Start a new Backtest
        </button>
      </div>

      {error && (
        <p className="text-red-500">
          Could not load data. Check your authentication.
        </p>
      )}
      {marketError && (
        <p className="text-red-500">
          Could not load market data. Check your backend server.
        </p>
      )}

      {marketData && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition">
            <div className="flex items-center gap-3 mb-2 text-green-400">
              <FiDollarSign className="text-xl" />
              <h2 className="text-lg font-semibold">
                Current Price ({marketData.symbol})
              </h2>
            </div>
            <p className="text-white text-xl font-bold">
              ${parseFloat(marketData.price).toFixed(2)}
            </p>
          </div>
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition">
            <div className="flex items-center gap-3 mb-2 text-blue-400">
              <FiTrendingUp className="text-xl" />
              <h2 className="text-lg font-semibold">Volume</h2>
            </div>
            <p className="text-white text-xl font-bold">
              {parseInt(marketData.volume).toLocaleString()}
            </p>
          </div>
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition">
            <div className="flex items-center gap-3 mb-2 text-yellow-400">
              <FiStar className="text-xl" />
              <h2 className="text-lg font-semibold">Symbol</h2>
            </div>
            <p className="text-white text-xl font-bold">
              {marketData.symbol}
            </p>
          </div>
        </div>
      )}

      {summary && !loading && !error && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition">
              <div className="flex items-center gap-3 mb-2 text-purple-400">
                <FiUser className="text-xl" />
                <h2 className="text-lg font-semibold">User</h2>
              </div>
              <p className="text-white text-xl font-bold">
                {summary.username}
              </p>
            </div>

            <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition">
              <div className="flex items-center gap-3 mb-2 text-blue-400">
                <FiTrendingUp className="text-xl" />
                <h2 className="text-lg font-semibold">Total Volume</h2>
              </div>
              <p className="text-white text-xl font-bold">
                ${summary.total_volume}
              </p>
            </div>

            <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition">
              <div className="flex items-center gap-3 mb-2 text-yellow-400">
                <FiStar className="text-xl" />
                <h2 className="text-lg font-semibold">Most Traded Asset</h2>
              </div>
              <p className="text-white text-xl font-bold">
                {summary.most_traded_asset || "None"}
              </p>
            </div>
          </div>

          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md">
            <h2 className="text-white text-lg font-semibold mb-4">
              Volume Evolution
            </h2>
            <Line data={chartData} />
          </div>
        </>
      )}
    </PageWrapper>
  );
}

export default Dashboard;