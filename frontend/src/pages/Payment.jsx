import React, { useState } from 'react';

const Payment = () => {
  const [cardNumber, setCardNumber] = useState('');
  const [expiry, setExpiry] = useState('');
  const [cvc, setCvc] = useState('');
  const [country, setCountry] = useState('Türkiye');
  const [orderId, setOrderId] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Sipariş numarası oluşturma simülasyonu
    setOrderId(Math.random().toString(36).substr(2, 9).toUpperCase());
  };

  if (orderId) {
    return (
      <div style={{ maxWidth: 400, margin: '3rem auto', padding: 32, border: '1px solid #eee', borderRadius: 8, textAlign: 'center' }}>
        <h2>Ödeme Başarılı!</h2>
        <p>Sipariş Numaranız: <b>{orderId}</b></p>
        <p>Siparişlerinizi <a href="/orders">Siparişlerim</a> sayfasından takip edebilirsiniz.</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 400, margin: '3rem auto', padding: 32, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Ödeme Bilgileri</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 16 }}>
          <label>Kart Numarası</label>
          <input type="text" value={cardNumber} onChange={e => setCardNumber(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <div style={{ flex: 1 }}>
            <label>Son Kullanma</label>
            <input type="text" value={expiry} onChange={e => setExpiry(e.target.value)} placeholder="AA/YY" required style={{ width: '100%', padding: 8, marginTop: 4 }} />
          </div>
          <div style={{ flex: 1 }}>
            <label>CVC</label>
            <input type="text" value={cvc} onChange={e => setCvc(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
          </div>
        </div>
        <div style={{ marginBottom: 16 }}>
          <label>Ülke</label>
          <select value={country} onChange={e => setCountry(e.target.value)} style={{ width: '100%', padding: 8, marginTop: 4 }}>
            <option value="Türkiye">Türkiye</option>
            <option value="ABD">ABD</option>
            <option value="Almanya">Almanya</option>
          </select>
        </div>
        <button type="submit" style={{ width: '100%', padding: 10, background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 4 }}>Ödeme Yap</button>
      </form>
    </div>
  );
};

export default Payment; 