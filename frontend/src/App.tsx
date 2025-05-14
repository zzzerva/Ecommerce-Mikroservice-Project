import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getCurrentUser } from './store/slices/authSlice';
import { RootState } from './store';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Header from './components/Header';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

const App: React.FC = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getCurrentUser());
  }, [dispatch]);

  return (
    <Router>
      <div>
        <Header />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            }
          />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                  <h1 className="text-3xl font-bold text-gray-900">Ana Sayfa</h1>
                </div>
              </PrivateRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App; 