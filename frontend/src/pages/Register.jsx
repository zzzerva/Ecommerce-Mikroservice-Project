import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Notification from '../components/Notification';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [notification, setNotification] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Kayıt işlemi burada yapılacak
    setNotification({
      message: 'Başarıyla kayıt olundu!',
      type: 'success'
    });

    // 2 saniye sonra login sayfasına yönlendir
    setTimeout(() => {
      navigate('/login');
    }, 2000);
  };

  return (
    <div style={{ maxWidth: 400, margin: '3rem auto', padding: 32, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Kayıt Ol</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 16 }}>
          <label>Ad Soyad</label>
          <input type="text" value={name} onChange={e => setName(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label>Email adresi</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label>Şifre</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <button type="submit" style={{ width: '100%', padding: 10, background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 4 }}>Kayıt Ol</button>
      </form>
      <div style={{ marginTop: 16, textAlign: 'center' }}>
        Zaten hesabınız var mı? <Link to="/login">Giriş Yap</Link>
      </div>

      {notification && (
        <Notification 
          message={notification.message} 
          type={notification.type} 
        />
      )}
    </div>
  );
};

export default Register; 