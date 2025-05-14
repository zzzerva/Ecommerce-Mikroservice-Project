import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const Checkout = () => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const { cart, removeFromCart, updateQuantity } = useCart();
  const navigate = useNavigate();

  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/payment');
  };

  if (cart.length === 0) {
    return (
      <div style={{ maxWidth: 600, margin: '3rem auto', textAlign: 'center', padding: 32 }}>
        <h2>Sepetiniz Boş</h2>
        <p style={{ marginBottom: 24 }}>Sepetinizde henüz ürün bulunmuyor.</p>
        <button 
          onClick={() => navigate('/')}
          style={{ 
            padding: '10px 24px', 
            background: '#4f46e5', 
            color: '#fff', 
            border: 'none', 
            borderRadius: 4,
            cursor: 'pointer'
          }}
        >
          Alışverişe Başla
        </button>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', maxWidth: 1000, margin: '3rem auto', gap: 32 }}>
      <form onSubmit={handleSubmit} style={{ flex: 1, padding: 32, border: '1px solid #eee', borderRadius: 8 }}>
        <h2>Kişisel Bilgiler</h2>
        <div style={{ marginBottom: 16 }}>
          <label>Ad Soyad</label>
          <input type="text" value={fullName} onChange={e => setFullName(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label>Email adresi</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label>Telefon</label>
          <input type="text" value={phone} onChange={e => setPhone(e.target.value)} style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label>Adres</label>
          <input type="text" value={address} onChange={e => setAddress(e.target.value)} style={{ width: '100%', padding: 8, marginTop: 4 }} />
        </div>
        <button type="submit" style={{ width: '100%', padding: 10, background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 4 }}>Devam Et</button>
      </form>
      <div style={{ width: 350, padding: 32, border: '1px solid #eee', borderRadius: 8, background: '#fafafa' }}>
        <h2>Sepet</h2>
        {cart.map(item => (
          <div key={item.id} style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
            <img src={item.image} alt={item.title} style={{ width: 60, height: 40, objectFit: 'cover', borderRadius: 4, marginRight: 12 }} />
            <div style={{ flex: 1 }}>
              <div>{item.title}</div>
              <div style={{ fontSize: 14, color: '#666' }}>{item.price} ₺</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <button 
                onClick={() => updateQuantity(item.id, item.quantity - 1)}
                style={{ 
                  padding: '4px 8px', 
                  background: '#f3f4f6', 
                  border: '1px solid #ddd',
                  borderRadius: 4,
                  cursor: 'pointer'
                }}
              >
                -
              </button>
              <span>{item.quantity}</span>
              <button 
                onClick={() => updateQuantity(item.id, item.quantity + 1)}
                style={{ 
                  padding: '4px 8px', 
                  background: '#f3f4f6', 
                  border: '1px solid #ddd',
                  borderRadius: 4,
                  cursor: 'pointer'
                }}
              >
                +
              </button>
            </div>
            <button 
              onClick={() => removeFromCart(item.id)}
              style={{ 
                marginLeft: 12, 
                padding: '4px 8px', 
                background: '#fee2e2', 
                color: '#dc2626',
                border: 'none',
                borderRadius: 4,
                cursor: 'pointer'
              }}
            >
              Kaldır
            </button>
          </div>
        ))}
        <hr />
        <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold', marginTop: 16 }}>
          <span>Toplam</span>
          <span>{subtotal} ₺</span>
        </div>
        <div style={{ fontSize: 12, color: '#888', marginTop: 8 }}>
          Kargo ve vergiler ödeme ekranında hesaplanacaktır.
        </div>
      </div>
    </div>
  );
};

export default Checkout; 