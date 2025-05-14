import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { logout } from '../store/slices/authSlice';
import { RootState } from '../store';

const Header: React.FC = () => {
  const [showProfile, setShowProfile] = useState(false);
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-xl font-bold text-gray-800">E-Commerce</h1>
            </div>
          </div>

          <div className="flex items-center">
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setShowProfile(!showProfile)}
                  className="flex items-center space-x-2 text-gray-700 hover:text-gray-900"
                >
                  <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white">
                    {user?.full_name.charAt(0).toUpperCase()}
                  </div>
                  <span>{user?.full_name}</span>
                </button>

                {showProfile && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
                    <div className="px-4 py-2 border-b">
                      <p className="text-sm font-medium text-gray-900">{user?.full_name}</p>
                      <p className="text-sm text-gray-500">{user?.email}</p>
                    </div>
                    <button
                      onClick={() => navigate('/profile')}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Profil
                    </button>
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Çıkış Yap
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex space-x-4">
                <button
                  onClick={() => navigate('/login')}
                  className="text-gray-700 hover:text-gray-900"
                >
                  Giriş Yap
                </button>
                <button
                  onClick={() => navigate('/register')}
                  className="text-gray-700 hover:text-gray-900"
                >
                  Kayıt Ol
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 