import React, { useState } from 'react';
import ProductCard from '../components/ProductCard';
import { useCart } from '../context/CartContext';
import Notification from '../components/Notification';

const sampleProducts = [
  { 
    id: 1, 
    title: 'MacBook Pro', 
    price: 1701, 
    image: 'https://dummyimage.com/300x200/ccc/fff&text=MacBook+Pro',
    category: 'electronics'
  },
  { 
    id: 2, 
    title: 'MacBook Air', 
    price: 989, 
    image: 'https://dummyimage.com/300x200/ccc/fff&text=MacBook+Air',
    category: 'electronics'
  },
  { 
    id: 3, 
    title: 'iPhone 9', 
    price: 7999, 
    image: 'https://dummyimage.com/300x200/ccc/fff&text=iPhone+9',
    category: 'electronics'
  },
  {
    id: 4,
    title: 'Suç ve Ceza',
    price: 45,
    image: 'https://dummyimage.com/300x200/ccc/fff&text=Suç+ve+Ceza',
    category: 'books'
  },
  {
    id: 5,
    title: 'Futbol Topu',
    price: 120,
    image: 'https://dummyimage.com/300x200/ccc/fff&text=Futbol+Topu',
    category: 'sports'
  },
  {
    id: 6,
    title: 'Yoga Matı',
    price: 85,
    image: 'https://dummyimage.com/300x200/ccc/fff&text=Yoga+Matı',
    category: 'sports'
  }
];

const categories = [
  { id: 'all', name: 'Tümü' },
  { id: 'electronics', name: 'Elektronik' },
  { id: 'books', name: 'Kitaplar' },
  { id: 'sports', name: 'Spor' }
];

const Home = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const { addToCart, notification } = useCart();

  const filteredProducts = selectedCategory === 'all'
    ? sampleProducts
    : sampleProducts.filter(product => product.category === selectedCategory);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Tüm Ürünler</h1>
      
      {/* Category Filter */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              style={{
                padding: '8px 16px',
                borderRadius: '4px',
                border: '1px solid #ddd',
                background: selectedCategory === category.id ? '#4f46e5' : 'white',
                color: selectedCategory === category.id ? 'white' : 'black',
                cursor: 'pointer'
              }}
            >
              {category.name}
            </button>
          ))}
        </div>
      </div>

      {/* Products Grid */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16 }}>
        {filteredProducts.map(product => (
          <ProductCard 
            key={product.id} 
            product={product} 
            onAddToCart={addToCart} 
          />
        ))}
      </div>

      {/* Notification */}
      {notification && (
        <Notification 
          message={notification.message} 
          type={notification.type} 
        />
      )}
    </div>
  );
};

export default Home; 