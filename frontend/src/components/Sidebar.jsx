import { useState } from "react";
import { Link } from "react-router-dom";
import { Home, BarChart, Bell, Settings, LogOut, Briefcase } from "lucide-react"; // Importe o ícone do portfólio

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div
      className={`bg-gray-800 h-screen p-4 flex flex-col transition-all duration-300 ${
        isOpen ? "w-64" : "w-16"
      }`}
    >
      {/* Botão toggle */}
      <button
        className="text-gray-400 hover:text-white mb-6"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? "«" : "»"}
      </button>

      <nav className="flex flex-col space-y-2 flex-1">
        <Link to="/dashboard" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
          <Home size={20} />
          {isOpen && <span>Dashboard</span>}
        </Link>
        <Link to="/strategies" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
          <BarChart size={20} />
          {isOpen && <span>Strategies</span>}
        </Link>
        <Link to="/notifications" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
          <Bell size={20} />
          {isOpen && <span>Notifications</span>}
        </Link>
        <Link to="/portfolio" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
          <Briefcase size={20} />
          {isOpen && <span>Portfolio</span>}
        </Link>
        <Link to="/backtest" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
          <Settings size={20} />
          {isOpen && <span>Backtest</span>}
        </Link>
      </nav>

      <button className="flex items-center space-x-2 p-2 text-red-400 hover:bg-gray-700 rounded">
        <LogOut size={20} />
        {isOpen && <span>Logout</span>}
      </button>
    </div>
  );
}