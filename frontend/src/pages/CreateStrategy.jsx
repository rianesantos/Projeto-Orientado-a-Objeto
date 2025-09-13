import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import PageWrapper from "../components/PageWrapper";
import LoadingSpinner from "../components/LoadingSpinner";
import { FiSave, FiXCircle } from "react-icons/fi";

function CreateStrategy() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const newStrategyData = {
      name,
      description,
      is_active: false, // New strategy starts inactive
    };

    try {
      // Makes a POST request to the API with the form data
      await api.post("/strategies/", newStrategyData);
      
      // Redirects user to strategies page after creation
      navigate("/strategies", { state: { message: "Strategy created successfully!" } });
    } catch (err) {
      console.error("Error creating strategy:", err.response?.data?.detail || err.message);
      setError("Failed to create strategy. Please check your data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white">Create New Strategy</h1>
        <p className="text-purple-400 mt-2 text-lg">
          Define the basic details for your new trading strategy.
        </p>
      </div>

      <div className="max-w-xl mx-auto p-8 bg-gray-800 rounded-lg shadow-lg">
        {error && (
          <div className="p-4 mb-4 text-sm text-red-500 rounded-lg bg-red-900/20" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-300">
              Strategy Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
              required
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-300">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              rows="3"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
            ></textarea>
          </div>

          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate("/strategies")}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-300 bg-gray-700 rounded-md hover:bg-gray-600 transition-colors"
              disabled={loading}
            >
              <FiXCircle /> Cancel
            </button>
            <button
              type="submit"
              className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 transition-colors ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
              disabled={loading}
            >
              {loading ? (
                <LoadingSpinner size="sm" />
              ) : (
                <>
                  <FiSave /> Save Strategy
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </PageWrapper>
  );
}

export default CreateStrategy;
