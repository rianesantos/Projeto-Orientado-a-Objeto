// src/App.jsx

import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from './context/AuthContext';
import Dashboard from "./pages/Dashboard";
import Strategies from "./pages/Strategies";
import CreateStrategy from "./pages/CreateStrategy";
import Portfolio from "./pages/Portfolio";
import Notifications from "./pages/Notifications";
import Backtest from "./pages/Backtest";
import Login from "./pages/Login";
import Register from "./pages/Register";

function App() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    // Displays a loading spinner while the authentication state is checked
    return <div>Loading...</div>;
  }

  return (
    <Routes>
      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} 
      />
      <Route 
        path="/register" 
        element={isAuthenticated ? <Navigate to="/dashboard" /> : <Register />} 
      />
      
      {/* Rotas privadas */}
      <Route 
        path="/dashboard" 
        element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/strategies" 
        element={isAuthenticated ? <Strategies /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/strategies/new" 
        element={isAuthenticated ? <CreateStrategy /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/portfolio" 
        element={isAuthenticated ? <Portfolio /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/notifications" 
        element={isAuthenticated ? <Notifications /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/backtest" 
        element={isAuthenticated ? <Backtest /> : <Navigate to="/login" />} 
      />
      
      {/* Redirecionamento padrão e para rotas inexistentes */}
      <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
      <Route path="*" element={<Navigate to="/dashboard" />} />
    </Routes>
  );
}

export default App;
