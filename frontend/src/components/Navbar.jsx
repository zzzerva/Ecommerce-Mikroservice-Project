import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const Navbar = () => {
  // Şimdilik giriş durumu için örnek bir state
  const [user, setUser] = useState(null); // { name: 'Demo Kullanıcı', isAdmin: true }
  const navigate = useNavigate();
  const { getTotalItems } = useCart();

  const handleLogout = () => {
    setUser(null);
    navigate('/');
  };

  const totalItems = getTotalItems();

  return (
    <nav style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 2rem', background: '#222', color: '#fff' }}>
      <div style={{ fontWeight: 'bold', fontSize: '1.5rem' }}>
        <Link to="/" style={{ color: '#fff', textDecoration: 'none' }}>z-erva</Link>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <Link to="/checkout" style={{ color: '#fff', textDecoration: 'none', position: 'relative' }}>
          Sepetim
          {totalItems > 0 && (
            <span style={{
              position: 'absolute',
              top: -8,
              right: -12,
              background: '#4f46e5',
              color: 'white',
              borderRadius: '50%',
              width: 20,
              height: 20,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 12
            }}>
              {totalItems}
            </span>
          )}
        </Link>
        {user ? (
          <>
            <Link to="/profile" style={{ color: '#fff', textDecoration: 'none' }}>Profil</Link>
            <button 
              onClick={handleLogout} 
              style={{ 
                background: 'transparent', 
                color: '#fff', 
                border: 'none', 
                cursor: 'pointer',
                padding: '4px 8px'
              }}
            >
              Çıkış Yap
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: '#fff', textDecoration: 'none' }}>Giriş Yap</Link>
            <Link to="/register" style={{ color: '#fff', textDecoration: 'none' }}>Kayıt Ol</Link>
          </>
        )}
        {user && user.isAdmin && (
          <Link to="/admin" style={{ color: '#fff', textDecoration: 'none' }}>Admin Paneli</Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar; 