import React from 'react';

const sampleProducts = [
  { id: 1, title: 'MacBook Pro', stock: 5, price: 1701 },
  { id: 2, title: 'MacBook Air', stock: 8, price: 989 },
  { id: 3, title: 'iPhone 9', stock: 12, price: 106 },
];

const sampleOrders = [
  { id: '123456', items: 'MacBook Pro', total: 1701, status: 'pending', date: '2023-05-13' },
  { id: '789012', items: 'iPhone 9', total: 106, status: 'delivered', date: '2023-05-10' },
];

const Admin = () => {
  return (
    <div style={{ maxWidth: 1100, margin: '3rem auto', padding: 32, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Admin Paneli</h2>
      <h3>Ürünler ve Stok Durumu</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: 32 }}>
        <thead>
          <tr style={{ background: '#f3f3f3' }}>
            <th>ID</th>
            <th>Ürün Adı</th>
            <th>Stok</th>
            <th>Fiyat</th>
          </tr>
        </thead>
        <tbody>
          {sampleProducts.map(product => (
            <tr key={product.id}>
              <td>{product.id}</td>
              <td>{product.title}</td>
              <td>{product.stock}</td>
              <td>{product.price} ₺</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3>Siparişler</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#f3f3f3' }}>
            <th>Sipariş No</th>
            <th>Ürünler</th>
            <th>Tutar</th>
            <th>Durum</th>
            <th>Tarih</th>
          </tr>
        </thead>
        <tbody>
          {sampleOrders.map(order => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.items}</td>
              <td>{order.total} ₺</td>
              <td>{order.status}</td>
              <td>{order.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Admin; 