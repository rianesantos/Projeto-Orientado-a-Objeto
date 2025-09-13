import { useEffect, useState } from "react";
import api from "../services/api";
import PageWrapper from "../components/PageWrapper";
import LoadingSpinner from "../components/LoadingSpinner";
import { FiPieChart, FiTrendingUp } from "react-icons/fi";

function Portfolio() {
  const [portfolio, setPortfolio] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    api.get("/portfolio/1")
      .then((res) => {
        setPortfolio(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading portfolio:", err);
        setError(true);
        setLoading(false);
      });
  }, []);

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white">Meu Portfólio 💼</h1>
        <p className="text-purple-400 mt-2 text-lg">Veja seus ativos e acompanhe o desempenho</p>
      </div>

      {loading && <LoadingSpinner message="Carregando portfólio..." />}
      {error && <p className="text-red-500">Falha ao carregar os dados.</p>}

      {!loading && !error && portfolio.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {portfolio.map((item) => (
            <div
              key={item.asset}
              className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition hover:scale-[1.02]"
            >
              <div className="flex items-center gap-3 mb-2 text-blue-400">
                <FiPieChart className="text-xl" />
                <h2 className="text-lg font-semibold">{item.asset}</h2>
              </div>
              <p className="text-gray-300 text-sm mb-1">Quantidade: {item.quantity}</p>
              <p className="text-gray-300 text-sm mb-1">Preço Médio: ${item.average_price}</p>
              <p className="text-sm font-semibold mt-2">
                {item.pnl >= 0 ? (
                  <span className="text-green-400">Lucro: +${item.pnl}</span>
                ) : (
                  <span className="text-red-400">Prejuízo: -${Math.abs(item.pnl)}</span>
                )}
              </p>
            </div>
          ))}
        </div>
      )}

      {!loading && !error && portfolio.length === 0 && (
        <p className="text-gray-400">Você ainda não possui ativos em carteira.</p>
      )}
    </PageWrapper>
  );
}

export default Portfolio;
