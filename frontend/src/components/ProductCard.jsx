import React from 'react';

const ProductCard = ({ product, onAddToCart }) => {
  return (
    <div style={{ border: '1px solid #eee', borderRadius: 8, padding: 16, width: 220, margin: 8, background: '#fff', boxShadow: '0 2px 8px #eee' }}>
      <img src={product.image} alt={product.title} style={{ width: '100%', height: 120, objectFit: 'cover', borderRadius: 4 }} />
      <h3 style={{ fontSize: 18, margin: '12px 0 4px 0' }}>{product.title}</h3>
      <div style={{ fontWeight: 'bold', fontSize: 16 }}>{product.price} ₺</div>
      <button onClick={() => onAddToCart(product)} style={{ marginTop: 12, width: '100%', padding: 8, background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 4 }}>
        Sepete Ekle
      </button>
    </div>
  );
};

export default ProductCard; 