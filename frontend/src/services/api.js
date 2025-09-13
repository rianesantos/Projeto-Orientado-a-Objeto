import axios from 'axios';
import { getAuthToken, setAuthToken } from '../utils/auth'; 

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      setAuthToken(null);
      window.location.href = '/login'; 
    }
    return Promise.reject(error);
  }
);

export default api;