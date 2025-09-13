import { useNavigate } from "react-router-dom";
import { FiEdit, FiTrash2, FiToggleRight, FiToggleLeft } from "react-icons/fi";
import api from "../services/api";

function StrategyCard({ strategy, onStrategyUpdate, onStrategyDelete }) {
  const navigate = useNavigate();

  const handleEdit = () => {
    navigate(`/strategies/edit/${strategy.id}`);
  };

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this strategy?")) {
      try {
        await api.delete(`/strategies/${strategy.id}`);
        // Chama a função de callback para atualizar a lista de estratégias
        onStrategyDelete(strategy.id); 
      } catch (error) {
        console.error("Failed to delete strategy:", error);
        alert("Failed to delete strategy. Please try again.");
      }
    }
  };

  const handleToggleStatus = async () => {
    try {
      const newStatus = !strategy.is_active;
      await api.put(`/strategies/${strategy.id}`, { ...strategy, is_active: newStatus });
      onStrategyUpdate(strategy.id, { is_active: newStatus });
    } catch (error) {
      console.error("Failed to toggle strategy status:", error);
      alert("Failed to change strategy status.");
    }
  };

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition hover:scale-[1.02]">
      <div className="flex items-center justify-between gap-3 mb-2 text-purple-400">
        <h2 className="text-lg font-semibold">{strategy.name}</h2>
        <div className="flex items-center gap-2">
          <button
            onClick={handleToggleStatus}
            className="text-gray-400 hover:text-green-500 transition"
            title={strategy.is_active ? "Deactivate Strategy" : "Activate Strategy"}
          >
            {strategy.is_active ? <FiToggleRight className="text-2xl" /> : <FiToggleLeft className="text-2xl" />}
          </button>
          <button
            onClick={handleEdit}
            className="text-gray-400 hover:text-blue-400 transition"
            title="Edit Strategy"
          >
            <FiEdit className="text-xl" />
          </button>
          <button
            onClick={handleDelete}
            className="text-gray-400 hover:text-red-500 transition"
            title="Delete Strategy"
          >
            <FiTrash2 className="text-xl" />
          </button>
        </div>
      </div>
      <p className="text-gray-300 text-sm mb-2">{strategy.description}</p>
      {/* <p className="text-blue-400 text-sm">Rule: {strategy.rule}</p> */}
      <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold mt-2 ${strategy.is_active ? "bg-green-500 text-white" : "bg-red-500 text-white"}`}>
        {strategy.is_active ? "Active" : "Inactive"}
      </span>
    </div>
  );
}

export default StrategyCard;