import React, { useState } from 'react';

const Profile = () => {
  const [activeTab, setActiveTab] = useState('profile'); // 'profile' veya 'orders'
  
  // Örnek kullanıcı bilgileri
  const user = {
    name: 'Demo Kullanıcı',
    email: 'demo@example.com',
    phone: '555-0123',
    address: 'Örnek Mahallesi, Örnek Sokak No:1'
  };

  // Örnek siparişler
  const orders = [
    {
      id: 1,
      date: '2024-03-15',
      total: 1850,
      status: 'Tamamlandı',
      items: [
        { title: 'Yoga Matı', quantity: 1, price: 85 },
        { title: 'Futbol Topu', quantity: 1, price: 120 }
      ]
    },
    {
      id: 2,
      date: '2024-03-14',
      total: 45,
      status: 'Kargoda',
      items: [
        { title: 'Suç ve Ceza', quantity: 1, price: 45 }
      ]
    }
  ];

  return (
    <div style={{ maxWidth: 800, margin: '3rem auto', padding: '0 1rem' }}>
      <div style={{ display: 'flex', gap: '2rem', marginBottom: '2rem' }}>
        <button
          onClick={() => setActiveTab('profile')}
          style={{
            padding: '8px 16px',
            background: activeTab === 'profile' ? '#4f46e5' : '#f3f4f6',
            color: activeTab === 'profile' ? 'white' : 'black',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Profil Bilgileri
        </button>
        <button
          onClick={() => setActiveTab('orders')}
          style={{
            padding: '8px 16px',
            background: activeTab === 'orders' ? '#4f46e5' : '#f3f4f6',
            color: activeTab === 'orders' ? 'white' : 'black',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Siparişlerim
        </button>
      </div>

      {activeTab === 'profile' ? (
        <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h2 style={{ marginBottom: '1.5rem' }}>Profil Bilgileri</h2>
          <div style={{ display: 'grid', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#666' }}>Ad Soyad</label>
              <div style={{ padding: '0.5rem', background: '#f9fafb', borderRadius: '4px' }}>{user.name}</div>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#666' }}>Email</label>
              <div style={{ padding: '0.5rem', background: '#f9fafb', borderRadius: '4px' }}>{user.email}</div>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#666' }}>Telefon</label>
              <div style={{ padding: '0.5rem', background: '#f9fafb', borderRadius: '4px' }}>{user.phone}</div>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', color: '#666' }}>Adres</label>
              <div style={{ padding: '0.5rem', background: '#f9fafb', borderRadius: '4px' }}>{user.address}</div>
            </div>
          </div>
        </div>
      ) : (
        <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h2 style={{ marginBottom: '1.5rem' }}>Siparişlerim</h2>
          {orders.map(order => (
            <div key={order.id} style={{ 
              border: '1px solid #eee', 
              borderRadius: '8px', 
              padding: '1rem', 
              marginBottom: '1rem' 
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div>
                  <div style={{ color: '#666' }}>Sipariş No: #{order.id}</div>
                  <div style={{ color: '#666' }}>Tarih: {order.date}</div>
                </div>
                <div>
                  <div style={{ fontWeight: 'bold' }}>{order.total} ₺</div>
                  <div style={{ 
                    color: order.status === 'Tamamlandı' ? '#059669' : '#d97706',
                    fontSize: '0.875rem'
                  }}>
                    {order.status}
                  </div>
                </div>
              </div>
              <div style={{ borderTop: '1px solid #eee', paddingTop: '1rem' }}>
                {order.items.map((item, index) => (
                  <div key={index} style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between',
                    marginBottom: '0.5rem'
                  }}>
                    <div>
                      {item.title} x {item.quantity}
                    </div>
                    <div>
                      {item.price * item.quantity} ₺
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Profile; 