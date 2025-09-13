import { Link, useLocation } from "react-router-dom";
import { FiHome, FiTrendingUp, FiPieChart, FiBell, FiActivity } from "react-icons/fi";

function Navbar() {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "Dashboard", icon: <FiHome /> },
    { path: "/strategies", label: "Strategies", icon: <FiTrendingUp /> },
    { path: "/portfolio", label: "Portfolio", icon: <FiPieChart /> },
    { path: "/notifications", label: "Notifications", icon: <FiBell /> },
    { path: "/backtest", label: "Backtest", icon: <FiActivity /> },
  ];

  return (
    <nav className="bg-gray-900 text-white px-6 py-4 fixed top-0 left-0 w-full shadow z-10">
      <div className="flex gap-6 items-center">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-2 hover:text-blue-400 ${
              location.pathname === item.path ? "text-blue-400 font-semibold" : ""
            }`}
          >
            {item.icon}
            {item.label}
          </Link>
        ))}
      </div>
    </nav>
  );
}

export default Navbar;
