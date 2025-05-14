import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const userApi = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

userApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

userApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

const productApi = axios.create({
  baseURL: process.env.REACT_APP_PRODUCT_API_URL || 'http://localhost:8001',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
const addAuthToken = (config: any) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};

// Response interceptor for handling errors
const handleResponseError = (error: any) => {
  if (error.response?.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
  }
  return Promise.reject(error);
};

productApi.interceptors.request.use(addAuthToken);
productApi.interceptors.response.use(undefined, handleResponseError);

export { userApi, productApi }; 