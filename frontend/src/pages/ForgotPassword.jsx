import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Şifre sıfırlama işlemi burada yapılacak
  };

  return (
    <div style={{ maxWidth: 400, margin: '3rem auto', padding: 32, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Şifremi Unuttum</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 16 }}>
          <label>Email adresi</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <button type="submit" style={{ width: '100%', padding: 10, background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 4 }}>Şifre Sıfırla</button>
      </form>
      <div style={{ marginTop: 16, textAlign: 'center' }}>
        <Link to="/login">Giriş Ekranına Dön</Link>
      </div>
    </div>
  );
};

export default ForgotPassword; 