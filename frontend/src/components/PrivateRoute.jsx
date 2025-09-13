import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../utils/auth';

function PrivateRoute({ children }) {
  const auth = isAuthenticated();
  return auth ? children : <Navigate to="/login" replace />;
}

export default PrivateRoute;