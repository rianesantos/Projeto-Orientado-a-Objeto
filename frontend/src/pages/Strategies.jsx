import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import PageWrapper from "../components/PageWrapper";
import StrategyCard from "../components/StrategyCard";
import LoadingSpinner from "../components/LoadingSpinner";
import { FiPlusCircle } from "react-icons/fi";

function Strategies() {
  const [strategies, setStrategies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const navigate = useNavigate();

  const fetchStrategies = async () => {
    setLoading(true);
    try {
      const res = await api.get("/strategies");
      setStrategies(res.data);
      setLoading(false);
    } catch (err) {
      console.error("Error loading strategies:", err);
      setError(true);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStrategies();
  }, []);

  // This function now just redirects to the creation page
  const handleCreateNewStrategy = () => {
    navigate("/strategies/new"); 
  };

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white">My Strategies 🎯</h1>
        <p className="text-purple-400 mt-2 text-lg">
          Manage and test your trading strategies
        </p>
      </div>

      <div className="mb-6">
        <button
          onClick={handleCreateNewStrategy}
          className="flex items-center gap-2 bg-blue-600 text-white px-5 py-2 rounded-md hover:bg-blue-700 hover:scale-105 transition-transform"
        >
          <FiPlusCircle className="text-lg" />
          Create new strategy
        </button>
      </div>

      {loading && <LoadingSpinner message="Loading strategies..." />}
      {error && <p className="text-red-500">Failed to load strategies.</p>}

      {!loading && !error && strategies.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {strategies.map((strategy) => (
            <StrategyCard key={strategy.id} strategy={strategy} />
          ))}
        </div>
      )}

      {!loading && !error && strategies.length === 0 && (
        <p className="text-gray-400">
          You haven't created any strategies yet.
        </p>
      )}
    </PageWrapper>
  );
}

export default Strategies;
