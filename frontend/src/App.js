import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { CartProvider } from './context/CartContext';
import { OrderProvider } from './context/OrderContext';
import Navbar from './components/Navbar';
import AppRoutes from './routes';

function App() {
  return (
    <Router>
      <CartProvider>
        <OrderProvider>
          <Navbar />
          <AppRoutes />
        </OrderProvider>
      </CartProvider>
    </Router>
  );
}

export default App;
