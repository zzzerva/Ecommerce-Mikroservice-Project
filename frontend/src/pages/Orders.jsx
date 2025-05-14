import React from 'react';

const sampleOrders = [
  { id: '123456', items: 'MacBook Pro', total: 1701, status: 'pending', date: '2023-05-13' },
  { id: '789012', items: 'iPhone 9', total: 106, status: 'delivered', date: '2023-05-10' },
];

const Orders = () => {
  return (
    <div style={{ maxWidth: 800, margin: '3rem auto', padding: 32, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Siparişlerim</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: 24 }}>
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

export default Orders; 