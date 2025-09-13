import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../utils/auth';

function PublicRoute({ children }) {
  const auth = isAuthenticated();
  return auth ? <Navigate to="/dashboard" replace /> : children;
}

export default PublicRoute;