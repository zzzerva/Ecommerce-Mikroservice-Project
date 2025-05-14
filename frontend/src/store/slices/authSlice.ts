import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { userApi } from '../../api/axios';

interface User {
  id: number;
  email: string;
  full_name: string;
  is_admin: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  loading: false,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials: (
      state,
      action: PayloadAction<{ user: User; token: string }>
    ) => {
      const { user, token } = action.payload;
      state.user = user;
      state.token = token;
      state.isAuthenticated = true;
      localStorage.setItem('token', token);
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      localStorage.removeItem('token');
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const { setCredentials, logout, setError, clearError } = authSlice.actions;

export const login = (email: string, password: string) => async (dispatch: any) => {
  try {
    const response = await userApi.post('/auth/login', { email, password });
    dispatch(setCredentials(response.data));
  } catch (error: any) {
    dispatch(setError(error.response?.data?.detail || 'Login failed'));
  }
};

export const getCurrentUser = () => async (dispatch: any) => {
  try {
    const response = await userApi.get('/users/me');
    dispatch(setCredentials({ user: response.data, token: localStorage.getItem('token')! }));
  } catch (error) {
    dispatch(logout());
  }
};

export default authSlice.reducer; 